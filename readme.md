# NVDA Remote Access
Version 2.0

Welcome to the NVDA Remote Access addon, which will allow you to connect to another computer running the free NVDA screen reader. It makes no difference whether you are across the room or across the world. Connecting is simple, and there are very few commands to remember. You can connect to another person's computer, or allow a trusted person to connect to your system to perform routine maintenance, diagnose a problem, or provide training.

## Before You Begin

You will need to have installed NVDA on both computers, and obtain the NVDA Remote Access addon.
The installation of both NVDA and the Remote Access addon are standard. If you need more information, this can be found in NVDA's User Guide.

## Updating

When updating the addon, if you have installed NVDA Remote on the secure desktop, it is recommended that you also update the copy on the secure desktop.
To do this, first update your existing addon. Then open the NVDA menu, preferences, General settings, and press the button labeled "Use currently saved settings on the logon and other secure screens (requires administrator privileges)".

## Starting a remote session through a relay server
### On the computer to be controlled
1. Open the NVDA menu, Tools, Remote, Connect.
2. Choose client in the first radio button.
3. Select Allow this machine to be controlled in the second set of radio buttons.
4. In the host field, enter the host of the server you are connecting to, for example nvdaremote.com. When the particular server uses an alternative port, you can enter the host in the form &lt;host&gt;:&lt;port&gt;, for example nvdaremote.com:1234.
5. Enter a key into the key field, or press the generate key button.
The key is what others will use to control your computer.
The machine being controlled and all its clients need to use the same key.
6. Press ok. Once done, you will hear a tone and connected.

### On the machine that is to be the controlling computer
1. Open the NVDA menu, Tools, Remote, Connect.
2. Choose client in the first radio button.
3. Select Control another machine in the second set of radio buttons.
4. In the host field, enter the host of the server you are connecting to, for example nvdaremote.com. When the particular server uses an alternative port, you can enter the host in the form &lt;host&gt;:&lt;port&gt;, for example nvdaremote.com:1234.
5. Enter a key into the key field, or press the generate key button.
The machine being controlled and all its clients need to use the same key.
6. Press ok. Once done, you will hear a tone and connected.

## Direct connections
The server option in the connect dialog allows you to set up a direct connection.
Once selecting this, select which mode your end of the connection wwill be in.
The other pperson will connect to you using the opposite.

Once the mode is selected, you can use the Get External IP button to get your external IP address and
make sure the port which is entered in the port field is forwarded correctly.
If portcheck detects that your port (6837 by default) is not reachable, a warning will appear.
Forward your port and try again.
Note: The process for forwarding ports is outside of the scope of this document. Please consult the information provided with your router for further instruction.

Enter a key into the key field, or press generate. The other person will need your external IP along with the key to connect. If you entered a port other than the default (6837) in the port field, make sure that the other person appends the alternative port to the host address in the form &lt;external ip&gt;:&lt;port&gt;.

Once ok is pressed, you will be connected.
When the other person connects, you can use NVDA Remote normally.

## Controlling the remote machine

Once the session is connected, the user of the controlling machine can press f11 to start controlling the remote machine (e.g. by sending keyboard keys or braille input).
When NVDA says controlling remote machine, the keyboard and braille display keys you press will go to the remote machine. Furthermore, when the controlling machine is using a braille display, information from the remote machine will be displayed on it. Press f11 again to stop sending keys and switch back to the controlling machine.
For best compatibility, please ensure that the keyboard layouts on both machines match.

## Sharing your session

To share a link so someone else can easily join your NVDA REMOTE session, select Copy Link from the Remote menu.
IF you are connected as the controlling computer, this link will allow someone else to connect and be controlled.
If instead you have set up your computer to be controlled, the link will allow people who you share it with to control your machine.
Many applications will allow users to activate this link automatically, but if it does not run from within a specific app, it can be coppied to the clipboard and run from the run dialog.


## Send Ctrl+Alt+Del
While sending keys, it is not possible to send the CTRL+Alt+del combination normally.
If you need to send CTRL+Alt+del, and the remote system is on the secure desktop, use this command.

## Remotely Controlling an Unattended Computer

Sometimes, you may wish to control one of your own computers remotely. This is especially helpful if you are traveling, and you wish to control your home PC from your laptop. Or, you may want to control a computer in one room of your house while sitting outside with another PC. A little advanced preparation makes this convenient and possible.

1. Enter the NVDA menu, and choose Tools, then Remote. Finally, press Enter on Options.
2. Check the box that says, "Auto connect to control server on startup".
3. Select whether to use a remote relay server or to locally host the connection. 
4. Select Allow this machine to be controlled in the second set of radio buttons.
5. If you host the connection yourself, you will need to ensure that the port entered in the port field (6837 by default) on the controlled machine can be accessed from the controlling machines.
6. If you wish to use a relay server, Fill in both the Host and Key fields, tab to OK, and press Enter. The Generate Key option is not available in this situation. It is best to come up with a key you will remember so you can easily use it from any remote location.

For advanced use, you can also configure NVDA Remote to automatically connect to a local or remote relay server in controlling mode. If you want this, select Control another machine in the second set of radio buttons.

Note: The autoconnect at startup-related options in the options dialog do not apply until NVDA is restarted.


## Muting Speech on the Remote Computer
If you do not wish to hear the remote computer's speech or NVDA specific sounds, simply access the NVDA menu, Tools, and Remote. Arrow down to Mute Remote, and press Enter. Please note that this option will not disable remote braille output to the controlling display when the controlling machine is sending keys.


## Ending a remote Session

To end a remote session, do the following:

1. On the controlling computer, press F11 to stop controlling the remote machine. You should hear or read the message: "Controlling local machine." If you instead hear or read a message that you are controlling the remote machine, press F11 once more.

2. Access the NVDA menu, then Tools, Remote, and press Enter on Disconnect.

## Push clipboard
The Push clipboard option in the remote menu allows you to push text from your clipboard.
when activated, any text on the clipboard will be pushed to the other machines.

## Configuring NVDA Remote to Work on a Secure Desktop

In order for NVDA Remote to work on the secure desktop, the addon must be installed in the NVDA running on the secure desktop.

1. From the NVDA menu, select Preferences, then General Settings.

2. Tab to the Use Currently Saved Settings on the Logon and Other Secure Screens (requires administrator privileges) button, and press Enter.

3. Answer Yes to the prompts regarding copying your settings and about copying plugins, and respond to the User Account Control prompt that may appear.
4. When settings are copied, press Enter to dismiss the OK button. Tab to OK and Enter once more to exit the dialog.

Once NVDA Remote is installed on the secure desktop, if you are currently being controlled in a remote session,
you will have speech and braille access to the secure desktop when switched to.

## Contributions
We would like to acknowledge the following contributors, among others, who helped make the NVDA Remote project a reality.

* Hai Nguyen Ly
* Chris Westbrook
* Thomas Huebner
* John F Crosotn III
* Darrell Shandrow
* D Williams
* Matthew McCubbin
* Jason Meddaugh
* ABDULAZIZ ALSHMASI.
* Tyler W Kavanaugh
* Casey Mathews
* Babbage B.V.
* Leonard de Ruijter

## Change Log

### Version 2.0

* Support for remote Braille
* Support for nvdaremote:// links
* Centered Dialogs to conform with the rest of NVDA
* Fixed portcheck to point at a domain we control, portcheck.nvdaremote.com
* Support automatically connecting to a control server in master mode
* Fixed rendering error in documentation
* Update to protocol version 2, which includes an origin field in every remote message
* Significant code cleanup allowing easier modifications in future

