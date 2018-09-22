import os
import sys
import base64
import hashlib
import threading
import time
import Queue
import ssl
import socket
import select
from collections import defaultdict, OrderedDict
from logging import getLogger
log = getLogger('transport')
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from spake2 import SPAKE2_A, SPAKE2_B
sys.path.remove(sys.path[-1])
import callback_manager
import pysodium
if pysodium.sodium_init() < 0:
	raise RuntimeError("Unable to call sodium_init")

PROTOCOL_VERSION = 2


class Transport(object):

	def __init__(self, serializer):
		self.serializer = serializer
		self.callback_manager = callback_manager.CallbackManager()
		self.connected = False
		self.successful_connects = 0

	def transport_connected(self):
		self.successful_connects += 1
		self.connected = True
		self.callback_manager.call_callbacks('transport_connected')

	def register_callback(self, event_type, callback):
		return self.callback_manager.register_callback(event_type, callback)

	def unregister_callback(self, event_type, callback):
		return self.callback_manager.unregister_callback(event_type, callback)

class TCPTransport(Transport):

	def __init__(self, serializer, address, timeout=0):
		super(TCPTransport, self).__init__(serializer=serializer)
		self.closed = False
		#Buffer to hold partially received data
		self.buffer = ""
		self.queue = Queue.Queue()
		self.address = address
		self.server_sock = None
		self.queue_thread = None
		self.timeout = timeout
		self.reconnector_thread = ConnectorThread(self)

	def run(self):
		self.closed = False
		try:
			self.server_sock = self.create_outbound_socket(self.address)
			self.server_sock.connect(self.address)
		except Exception as e:
			self.callback_manager.call_callbacks('transport_connection_failed')
			raise
		self.transport_connected()
		self.queue_thread = threading.Thread(target=self.send_queue)
		self.queue_thread.daemon = True
		self.queue_thread.start()
		while self.server_sock is not None:
			try:
				readers, writers, error = select.select([self.server_sock], [], [self.server_sock])
			except socket.error:
				self.buffer = ""
				break
			if self.server_sock in error:
				self.buffer = ""
				break
			if self.server_sock in readers:
				try:
					self.handle_server_data()
				except socket.error:
					self.buffer = ""
					break
		self.connected = False
		self.callback_manager.call_callbacks('transport_disconnected')
		self._disconnect()

	def create_outbound_socket(self, address):
		address = socket.getaddrinfo(*address)[0]
		server_sock = socket.socket(*address[:3])
		if self.timeout:
			server_sock.settimeout(self.timeout)
		server_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		server_sock.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60000, 2000))
		server_sock = ssl.wrap_socket(server_sock)
		return server_sock

	def handle_server_data(self):
		data = self.buffer + self.server_sock.recv(16384)
		self.buffer = ""
		if data == '':
			self._disconnect()
			return
		if '\n' not in data:
			self.buffer += data
			return
		while '\n' in data:
			line, sep, data = data.partition('\n')
			self.parse(line, self.callback_manager)
		self.buffer += data

	def parse(self, line, callback_manager, **kwargs):
		if not line:
			return
		obj = self.serializer.deserialize(line)
		if 'type' not in obj:
			return
		obj.update(kwargs)
		callback = "msg_"+obj['type']
		del obj['type']
		callback_manager.call_callbacks(callback, **obj)

	def send_queue(self):
		while True:
			item = self.queue.get()
			if item is None:
				return
			try:
				self.server_sock.sendall(item)
			except socket.error:
				return

	def send(self, type, **kwargs):
		obj = self.serializer.serialize(type=type, **kwargs)
		if self.connected:
			self.queue.put(obj)

	def _disconnect(self):
		"""Disconnect the transport due to an error, without closing the connector thread."""
		if not self.connected:
			return
		if self.queue_thread is not None:
			self.queue.put(None)
			self.queue_thread.join()
		clear_queue(self.queue)
		self.server_sock.close()
		self.server_sock = None

	def close(self):
		self.callback_manager.call_callbacks('transport_closing')
		self.reconnector_thread.running = False
		self._disconnect()
		self.closed = True
		self.reconnector_thread = ConnectorThread(self)

class RelayTransport(TCPTransport):

	def __init__(self, serializer, address, timeout=0, channel=None, connection_type=None, protocol_version=PROTOCOL_VERSION):
		super(RelayTransport, self).__init__(address=address, serializer=serializer, timeout=timeout)
		log.info("Connecting to %s channel %s" % (address, channel))
		self.channel = channel
		self.connection_type = connection_type
		self.protocol_version = protocol_version
		self.callback_manager.register_callback('transport_connected', self.on_connected)

	def on_connected(self):
		self.send('protocol_version', version=self.protocol_version)
		if self.channel is not None:
			self.send('join', channel=self.channel, connection_type=self.connection_type)
		else:
			self.send('generate_key')

class EncryptedRelayTransport(RelayTransport):

	PADDING_BLOCKSIZE = 16

	def __init__(self, *args, **kwargs):
		super(EncryptedRelayTransport, self).__init__(*args, **kwargs)
		# A map of slave IDs to spake2 instances
		self.key_map = {}
		# Map of client IDs to session keys
		self.session_keys = {}
		self.my_id = 0
		self.hashed_channel = e2e_channel_from_key(self.channel)
		self.callback_manager.register_callback('msg_channel_joined', self.handle_channel_joined)
		self.callback_manager.register_callback('msg_client_joined', self.handle_client_joined)
		self.callback_manager.register_callback('msg_client_left', self.handle_client_left)
		self.callback_manager.register_callback('msg_get_enc_key', self.handle_get_enc_key)
		self.callback_manager.register_callback('msg_put_enc_key', self.handle_put_enc_key)
		self.callback_manager.register_callback('msg_e2e_message', self.handle_e2e_message)
		self.encrypted_callback_manager = callback_manager.CallbackManager()
		self.clients = OrderedDict()
		self.coordinator = None
		self.key_sequence = -1
		self.key_sequence_map = {}

	def on_connected(self):
		self.send_unencrypted('protocol_version', version=self.protocol_version)
		if self.channel is not None:
			self.send_unencrypted('join', channel=self.hashed_channel, connection_type=self.connection_type)
		else:
			self.send_unencrypted('generate_key')

	IGNORED_CALLBACKS = ('msg_version_mismatch', 'msg_motd', 'transport_connected', 'transport_connection_failed', 'transport_closing', 'transport_disconnected')

	def register_callback(self, event_type, callback):
		if event_type in self.IGNORED_CALLBACKS:
			return self.callback_manager.register_callback(event_type, callback)
		return self.encrypted_callback_manager.register_callback(event_type, callback)

	def unregister_callback(self, event_type, callback):
		if event_type in self.IGNORED_CALLBACKS:
			return self.callback_manager.unregister_callback(event_type, callback)
		return self.encrypted_callback_manager.unregister_callback(event_type, callback)

	def handle_channel_joined(self, origin=None, clients=None, **kwargs):
		if clients is None:
			clients = []
		self.my_id = origin
		self.coordinator = self.my_id
		# Since noone's in the channel, we're the coordinator and implicitly authenticated
		if not clients:
			self.encrypted_callback_manager.call_callbacks('msg_channel_joined', origin=origin, clients=clients, **kwargs)
		for client in clients:
			self.clients[client['id']] = client
			self.clients[client['id']]['status'] = 'joined'
		self.clients[self.my_id] = {'id': self.my_id, 'connection_type': self.connection_type}
		self.update_coordinator()

	def handle_client_joined(self, client=None, **kwargs):
		client['status'] = 'joined'
		self.clients[client['id']] = client

	def handle_client_left(self, client=None, **kwargs):
		if client['id'] in self.clients and self.clients[client['id']].get('status') == 'authenticated':
			self.encrypted_callback_manager.call_callbacks('msg_client_left', client=client, **kwargs)
		if client['id'] in self.clients and client['id'] != self.my_id:
			del self.clients[client['id']]
		if client['id'] in self.key_map:
			del self.key_map[client['id']]
		if client['id'] in self.session_keys:
			del self.session_keys[client['id']]
		if self.key_sequence in self.key_sequence_map and client['id'] in self.key_sequence_map[self.key_sequence]['expected_nonce_map']:
			del self.key_sequence_map[self.key_sequence]['expected_nonce_map'][client['id']]
		self.update_coordinator()

	def handle_e2e_message(self, origin=None, msg=None, key_sequence=None, iv=None, **kwargs):
		if key_sequence is None:
			return
		if key_sequence not in self.key_sequence_map:
			return # We don't have the encryption key for this key sequence
		expected_nonce_map = self.key_sequence_map[key_sequence]['expected_nonce_map']
		expected_nonce = expected_nonce_map.get(origin)
		got_iv = False
		if expected_nonce is None:
			if iv is None:
				return # No nonce and none was provided, ignore the message
			iv = base64.b64decode(iv)
			if iv in self.key_sequence_map[self.key_sequence]['ivs']:
				return # Already seen this IV, could be a replay
			got_iv = True
			expected_nonce = iv

		try:
			decoded = base64.b64decode(msg)
			data = self.decrypt(decoded, expected_nonce, self.key_sequence_map[self.key_sequence]['k'])
			data = pysodium.unpad(data, self.PADDING_BLOCKSIZE)
		except ValueError:
			return # Can't decrypt the message
		if got_iv:
			if data[0] != '\x01':
				return # Not the initial message
			self.key_sequence_map[self.key_sequence]['ivs'].add(expected_nonce)
		expected_nonce_map[origin] = pysodium.increment(expected_nonce)
		self.callback_manager.call_callbacks('parsed', line=data[1:])
		super(EncryptedRelayTransport, self).parse(data[1:], self.encrypted_callback_manager, origin=origin)

	def update_coordinator(self):
		# The coordinator is the first client to join the channel.
		coordinator = self.clients.keys()[0]
		# If we are the coordinator, or the coordinator is unchanged,
		# We don't need to ask for a new session key.
		if coordinator == self.coordinator or coordinator == self.my_id:
			self.coordinator = coordinator
			return
		self.coordinator = coordinator
		self.key_map[coordinator] = SPAKE2_A(self.channel.encode('utf-8'))
		msg = self.key_map[coordinator].start()
		b64 = base64.b64encode(msg)
		log.debug("Sending first key exchange message to coordinator %d", coordinator)
		self.send_unencrypted(type='get_enc_key', msg=b64)

	def send(self, type, **kwargs):
		if self.key_sequence not in self.key_sequence_map:
			return
		nonce = self.key_sequence_map[self.key_sequence].get('nonce')
		include_nonce = False
		if nonce is None:
			nonce = self.get_random_nonce()
			include_nonce = True
		obj = self.serializer.serialize(type=type, **kwargs)
		initial_byte = ('\x01' if include_nonce else '\x00')
		obj = pysodium.pad(initial_byte + obj, self.PADDING_BLOCKSIZE)
		encrypted_obj = self.encrypt(obj, nonce, self.key_sequence_map[self.key_sequence]['k'])
		d = {}
		if include_nonce:
			d['iv'] = base64.b64encode(nonce)
		self.send_unencrypted(type='e2e_message', msg=base64.b64encode(encrypted_obj), key_sequence=self.key_sequence, **d)
		self.key_sequence_map[self.key_sequence]['nonce'] = pysodium.increment(nonce)

	def handle_get_enc_key(self, origin=None, msg=None, **kwargs):
		"""Sent by the master to negotiate a temporary session key with the slave."""
		if self.my_id != self.coordinator:
			return
		# Key negotiation as the slave needs SPAKE2_B
		s2 = SPAKE2_B(self.channel.encode('utf-8'))
		our_msg = s2.start()
		key = s2.finish(base64.b64decode(msg))
		self.session_keys[origin] = key
		# Increment our key sequence, and rekey everyone.
		self.key_sequence += 1
		log.debug("Generating new key sequence %d", self.key_sequence)
		self.key_sequence_map[self.key_sequence]= {}
		self.key_sequence_map[self.key_sequence]['k'] = pysodium.randombytes(pysodium.crypto_secretbox_KEYBYTES)
		self.key_sequence_map[self.key_sequence]['ivs'] = set()
		# Maps client IDs to expected nonces
		self.key_sequence_map[self.key_sequence]['expected_nonce_map'] = {}
		log.debug("Generated new k")
		# Send the second part of the key negotiation, with the encrypted channel key
		# Generate the map of k, encrypted with all the session keys
		key_map = {}
		k = self.key_sequence_map[self.key_sequence]['k']
		for id, session_key in self.session_keys.iteritems():
			nonce = self.get_random_nonce()
			encrypted_k = self.encrypt(k, nonce, session_key)
			key_map[id] = base64.b64encode(nonce + encrypted_k)
		self.send_unencrypted(type='put_enc_key', key_sequence=self.key_sequence, id_to=origin, msg=base64.b64encode(our_msg), enc_keys=key_map)
		log.debug("Sent put_enc_key to %d, sequence %d", origin, self.key_sequence)
		if origin in self.clients and self.clients[origin].get('status') == 'joined':
			self.clients[origin]['status'] = 'authenticated'
			self.encrypted_callback_manager.call_callbacks('msg_client_joined', client=self.clients[origin])

	def handle_put_enc_key(self, origin=None, id_to=None, msg=None, enc_keys=None, key_sequence=None, **kwargs):
		"""Message received by non-coordinators when the coordinator has finished the key negotiation."""
		# Receiving session key from coordinator for the first time
		if self.my_id == id_to and origin not in self.session_keys:
			session_key = self.key_map[origin].finish(base64.b64decode(msg))
			self.session_keys[origin] = session_key
		else:
			# If we have a session key from the coordinator, we need it to decrypt k.
			session_key = self.session_keys.get(origin)
		if session_key is None:
			# No session key received, and this was addressed to someone else.
			return
		if enc_keys:
			enc_keys = {int(k): v for k,v in enc_keys.iteritems()}
		if self.key_sequence == -1 and id_to == self.my_id:
			for id in enc_keys.keys() + [origin]:
				if id in self.clients:
					self.clients[id]['status'] = 'authenticated'
			clients = [self.clients[c] for c in self.clients if c != self.my_id and self.clients[c].get('status') == 'authenticated']
			self.encrypted_callback_manager.call_callbacks('msg_channel_joined', clients=clients)
		if id_to != self.my_id and id_to in self.clients and self.clients[id_to].get('status') == 'joined':
			self.clients[id_to]['status'] = 'authenticated'
			self.encrypted_callback_manager.call_callbacks('msg_client_joined', client=self.clients[id_to])


		k = None
		try:
			encrypted_k = enc_keys[self.my_id]
			encrypted_k = base64.b64decode(encrypted_k)
			nonce = encrypted_k[:pysodium.crypto_secretbox_NONCEBYTES]
			encrypted_k = encrypted_k[pysodium.crypto_secretbox_NONCEBYTES:]
			k = self.decrypt(encrypted_k, nonce, session_key)
		except (KeyError, ValueError):
			log.debug("K couldn't be decrypted")
			return
		self.key_sequence = key_sequence
		self.key_sequence_map[self.key_sequence] = {
			'k': k,
			'ivs': set(),
			'expected_nonce_map': {},
		}
		log.debug("Negotiated channel key")

	def send_unencrypted(self, type, **kwargs):
		super(EncryptedRelayTransport, self).send(type, **kwargs)

	def get_random_nonce(self):
		return pysodium.randombytes(pysodium.crypto_secretbox_NONCEBYTES)

	def encrypt(self, message, nonce, key):
		"""Encrypts a message."""
		return pysodium.crypto_secretbox(message, nonce, key)

	def decrypt(self, message, nonce, key):
		"""Decrypts a message."""
		return pysodium.crypto_secretbox_open(message, nonce, key)

	def run(self):
		self.key_map = {}
		self.session_keys = {}
		self.clients = OrderedDict()
		self.coordinator = None
		self.key_sequence = -1
		self.key_sequence_map = {}
		super(EncryptedRelayTransport, self).run()

class ConnectorThread(threading.Thread):

	def __init__(self, connector, connect_delay=5):
		super(ConnectorThread, self).__init__()
		self.connect_delay = connect_delay
		self.running = True
		self.connector = connector
		self.name = self.name + "_connector_loop"
		self.daemon = True

	def run(self):
		while self.running:
			try:
				self.connector.run()
			except socket.error:
				time.sleep(self.connect_delay)
				continue
			else:
				time.sleep(self.connect_delay)
		log.info("Ending control connector thread %s" % self.name)

def clear_queue(queue):
	try:
		while True:
			queue.get_nowait()
	except:
		pass

def e2e_channel_from_key(key):
	return "E2E_" + hashlib.pbkdf2_hmac('sha256', key.encode('utf-8'), 'NVDA_REMOTE_SALT', 500000).encode('hex')

def generate_key(keylen=9, alphabet="abcdefghijklmnopqrstuvwxyz0123456789"):
	def rand():
		while True:
			yield pysodium.randombytes(1)

	key = []
	for b in rand():
		if ord(b) >= (256//len(alphabet)) * len(alphabet):
			continue
		key.append(alphabet[ord(b) % len(alphabet)])
		if len(key) >= keylen:
			return "".join(key)
