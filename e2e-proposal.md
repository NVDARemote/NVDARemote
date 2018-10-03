title: End to End Encryption in NVDA Remote
author: Niko Carpenter <nikoacarpenter@gmail.com> and Tyler Spivey <tspivey@pcdesk.net>

# End to End Encryption in NVDA Remote
#### by Niko Carpenter <nikoacarpenter@gmail.com> and Tyler Spivey <tspivey@pc-desk.net>

## Background
Currently, [NVDA Remote][] is not encrypted end to end. In addition, the mechanism for authentication is a passphrase,
called the *key*, but that key is sent to the server in the clear. Finally, the controlled machine--*slave*--
does not verify that the controlling machine--*master*--knows the key--it trusts the server to perform that check.

This design has several flaws:
1. The server is the central point of trust for both the slave and master.
    * The slave cannot verify that the other party is really authorized to control it.
        This allows a malicious server, or anyone in the middle, to send commands to any connected slave.
    * The master cannot verify who it's controlling.
        An attacker who has figured out the key can set up a malicious look-alike slave and log passwords and other confidential information that
        the person at the master's keyboard can be tricked into typing.

2. The server can silently intercept and log any traffic passing through it.
    Even if users trust the owner of the server they're connecting to, hosts like nvdaremote.com are
    prime targets for attackers to infiltrate, given the amount of traffic passing through them.

3. It is strongly recommended that anyone using NVDA Remote choose a unique, randomly generated, strong passphrase as their key.
    Unfortunately, many people ignore this advice and reuse weak passwords.
    Since the server receives keys in the clear, users' passwords, many of which they use on other sites, will be viewable by the server owner or any attacker in the machine running the server.
    No keys are being written to the hard drive on the server end, but it would be preferable not to see these keys in the first place.

4. Given the high degree of trust required of servers, server owners can be deemed liable, if users accuse them of abuse or mismanagement
    leading to the loss of confidential data or misuse of their machines.

## Solution Overview
Clients will join a channel based on their passphrase, where the passphrase cannot be determined from the channel name.
Coordinators will generate a new shared encryption key any time a new client joins.
All non-coordinators will receive this same key, itself encrypted with a session key that they negotiated with the coordinator when they joined the channel.

### Note about the term *passphrase*
This document uses the term *passphrase* in place of *key*, used by legacy versions of NVDA Remote.
This helps differentiate between the secret that clients share to talk to each other
and keys used for encryption, which are not part of the user experience.

It is recommended, however, that the term *key* be renamed *passphrase* in the UI as well,
because users will be more familiar with the term *passphrase* and its security implications.

## Design
### Channels
Both masters and slaves will connect to an NVDA Remote server and join a channel based on a shared passphrase.
The passphrase will be used to create a key using [PBKDF2][]
with 500,000 rounds, which takes around 1 second on most systems to generate,
and a salt of *NVDA_REMOTE_SALT*.
*E2E_* plus this key, hex encoded, will be the name of the channel used on the server.

### Coordinators
The coordinator is a client responsible for managing encryption keys
and session keys with all other clients in the channel.
The first client to join a channel is the coordinator.
If there are still clients in the channel when the coordinator leaves,
the next earliest joiner will become the coordinator.
Coordinator status is agreed upon by clients. Servers are only responsible for
telling new joiners the correct join order of existing clients in a channel.

### Establishing a session
When a client connects to a non-empty channel,
or when a different client becomes coordinator, the client will request the encryption key from the coordinator via the *get_enc_key* message.
To do this without the server seeing the key, the requester and coordinator will perform an authenticated key exchange using [Spake2][].
The requester will play the *SPAKE2_A* role and get an output message. The following will be sent to the coordinator:

    {
        "type": "get_enc_key",
        "id_to": <uid-of-coordinator>,
        "message": <out-msg-from-SPAKE2>
    }

Upon receiving this message, the coordinator will see if the id_to is addressed to it.
If so, the coordinator, as *SPAKE2_B*, will get its own output message and use the output message from the requester to get a session key.
At this point, a new encryption key will be generated, the key sequence will be incremented,
and all other clients will be given this new encryption key via their session key.
This key will be shared between the coordinator and all other clients but will only be used for a single key sequence for forward secrecy.

As soon as a new client joins, the key sequence is incremented, and a new encryption key is generated,
to help prevent replay attacks.

The *put_enc_key* message sends the second half of the key exchange to the requester that sent *get_enc_key*.
It also contains the encryption key, itself encrypted with each non-coordinator’s session key,
and the new key sequence.
Non-coordinators will try decrypting each encryption key, until they can decrypt the key successfully.
*put_enc_key* looks like the following:

    {
        "type": "put_enc_key",
        "id_to": <uid-of-requester>,
        "message": <out-msg-from-SPAKE2>,
        "key_sequence": <key-sequence-starting-from-0>,
        "authorized_ids": [<id-of-client-with-session-key>...],
        enc_keys: [
            <nonce-plus-encryption-key-encrypted-with-session-key1>,
            <nonce-plus-encryption-key-encrypted-with-session-key2>,
            ...
        ]
    }

Clients get new encryption keys from all *put_enc_key* messages,
but only messages with *id_to* addressed to them are used for establishing a new session key.
The session key is unique between a single client and the coordinator and is only used to send the client the encryption key.
A new session key will be negotiated if the client reconnects.
All subsequent messages will be encrypted with the shared encryption key.
The *authorized_ids* list in *put_enc_key* is used by new joiners
to see which clients can receive encrypted messages.
If the coordinator has a session key with another client, that client's ID will be included in *authorized_ids*.

### Preventing replay attacks
Each time a different coordinator is chosen, all other clients will renegotiate a session key with the new coordinator, and a new encryption key and key sequence will be used.
Each time a new non-coordinator connects, the coordinator will change the encryption key, increment the key sequence, and rekey all other clients with their session keys.
This prevents new joiners from being able to decrypt messages that were sent to them before they established a session key with the coordinator.

Clients all hold, for each key sequence, a copy of the encryption key, the nonce for encrypting, the expected nonce for each participant by client ID, and a set of initialization vectors for each participant.
If a message is received from a client whose expected nonce is unknown,
the initialization vector, *iv*, in the message will be used to decrypt, if one was provided.
If the iv was already seen, this message will be dropped, as this could be a replay.
Upon successful decryption of a message,
the first byte of the plain text is checked to see if this message was the sending client's initial message for this key sequence (0x01).
If not (first byte will usually be 0x00), the message is dropped, since an attacker could be trying to pass it off as another client's initial message to replay it.
Otherwise, the iv is added to the set of initialization vectors,
and its incremented value is stored as the client's expected nonce.

If a message is received from a client whose expected nonce is known,
that nonce will be used for decryption.
When a message was successfully decrypted, the expected nonce will be incremented.
Any iv provided in *e2e_message* will be ignored, when the expected nonce is known.

If a message is received with a key sequence where the encryption key is not known, the message will be ignored.

### Encrypted messages
Libsodium secret boxes will be used for encrypting and decrypting messages.
The ciphertext will be base64 encoded for safe inclusion in a json object.

Other than transport layer messages like pings, joins, and key negotiations,
all messages will be encrypted and wrapped in an outer json object, with the type *e2e_message*.
Before encryption, if the encryption nonce has not been set, one will be randomly generated, and it will be included in *e2e_message* as *iv*--the initialization vector.
Post encryption, the encryption nonce will be incremented.

For example, if the master wants to send the letter *a*, the client will generate the following json:

    {
        "extended": false,
        "vk_code": 65,
        "scan_code": 30,
        "pressed": true,
        "type": "key"
    }

The above message will be encrypted with the shared encryption key, base64 encoded, and wrapped in an outer message:

    {
        "type": "e2e_message",
        "message": <base64-encoded-0x00-and-ciphertext>
    }

or if this was the first message the client sent for this key sequence,
it will include a base64 encoded initialization vector:

    {
        "type": "e2e_message",
        "iv": <base64-encoded-initialization-vector>,
        "message": <base64-encoded-0x01-and-ciphertext>
    }

### Key generation
Functionality for the *Generate Key* button in NVDA Remote's connect dialog
will be moved from the server to the client, to ensure the server doesn't know
which passphrases are being used. A 9-character passphrase containing
lowercase letters a-z and digits 0-9 will be generated locally.

### Backwards compatibility
Versions of NVDA Remote that support end to end encryption will not be compatible with versions that do not.
Furthermore, these newer versions will not work correctly with older servers.
Old versions of NVDA Remote will function normally with new servers,
however, servers should encourage older clients to upgrade to new versions of NVDA Remote.
This can be achieved by sending a message of the day with force_display = true
to clients after joining a channel, if the channel name does not begin with
*E2E_*, or its total length is not 68.

[NVDA Remote]: https://nvdaremote.com
[PBKDF2]: https://en.wikipedia.org/wiki/PBKDF2
[Spake2]: https://github.com/warner/python-spake2
