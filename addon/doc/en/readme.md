#NVDA Remote Access
Version 1.0

Welcome to the NVDA Remote Access addon, which will allow you to connect to another computer running the free NVDA screen reader. It makes no difference whether you are across the room or across the world. Connecting is simple, and there are very few commands to remember. You can connect to another person's computer, or allow a trusted person to connect to your system to perform routine maintenance, diagnose a problem, or provide training.

##Before You Begin

You will need to have installed NVDA on both computers, and obtain the NVDA Remote Access addon.
The installation of both NVDA and the Remote Access addon are standard. If you need more information, this can be found in NVDA's User Guide.

##Starting a remote session through a relay server
###Controlled	 computer
1. Open the NVDA menu, Tools, Remote, Connect.
2. Choose client in the first radio button.
3. Select Allow this machine to be controlled in the second set of radio buttons.
4. In the host field, enter the host of the server you are connecting to, for example nvdaremote.com.
5. Enter a key into the key field, or press the generate key button.
The key is what others will use to control your computer.
The machine being controlled and all its clients need to use the same key.
6. Press ok. Once done, you will hear a tone and connected.

###Controlling computer
1. Open the NVDA menu, Tools, Remote, Connect.
2. Choose client in the first radio button.
3. Select Control another machine in the second set of radio buttons.
4. In the host field, enter the host of the server you are connecting to, for example nvdaremote.com.
5. Enter a key into the key field, or press the generate key button.
The machine being controlled and all its clients need to use the same key.
6. Press ok. Once done, you will hear a tone and connected.

##Direct connections
The server option in the connect dialog allows you to set up a direct connection.
Once selecting this, select which mode your end of the connection wwill be in.
The other pperson will connect to you using the opposite.

Once the mode is selected, you can use the Get External IP button to get your external IP address and
make sure the port is forwarded correctly.
If portcheck detects that your port (6837) is not reachable, a warning will appear.
Forward your port and try again.
Note: The process for forwarding ports is outside of the scope of this document. Please consult the information provided with your router for further instruction.

Enter a key into the key field, or press generate. The other person will need your external IP along with the key to connect.

Once ok is pressed, you will be connected.
When the other person connects, you can use NVDA Remote normally.

##Sending keys
Once the session is connected, the controlling machine can then press f11 to start sending keys.
When NVDA says sending keys, the keys you press will go to the remote machine. Press f11 again to stop sending keys and switch back to the controlling machine.
For best compatibility, please ensure that the keyboard layouts on both machines match.

##Send Ctrl+Alt+Del
While sending keys, it is not possible to send the CTRL+Alt+del combination normally.
If you need to send CTRL+Alt+del, and the remote system is on the secure desktop, use this command.

##Remotely Controlling an Unattended Computer

Sometimes, you may wish to control one of your own computers remotely. This is especially helpful if you are traveling, and you wish to control your home PC from your laptop. Or, you may want to control a computer in one room of your house while sitting outside with another PC. A little advanced preparation makes this convenient and possible.

1. Enter the NVDA menu, and choose Tools, then Remote. Finally, press Enter on Options.
2. Check the box that says, "Auto connect to control server on startup".
3. Fill in the Host and Key fields, tab to OK, and press Enter.
4. Please note: the Generate Key option is not available in this situation. It is best to come up with a key you will remember so you can easily use it from any remote location.

##Muting Speech on the Remote Computer
If you do not wish to hear the remote computer's speech, simply access the NVDA menu, Tools, and Remote. Arrow down to Mute Remote Speech, and press Enter.


##Ending a remote Session

To end a remote session, do the following:

1. On the controlling computer, press F11 to stop sending keys. You should hear the message: "Not sending keys." If you instead hear a message that you are sending keys, press F11 once more.

2. Access the NVDA menu, then Tools, Remote, and press Enter on Disconnect.

##Push clipboard
The Push clipboard option in the remote menu allows you to push text from your clipboard.
when activated, any text on the clipboard will be pushed to the other machines.

##Configuring NVDA Remote to Work on a Secure Desktop

In order for NVDA Remote to work on the secure desktop, the addon must be installed in the NVDA running on the secure desktop.

1. From the NVDA menu, select Preferences, then General Settings.

2. Tab to the Use Currently Saved Settings on the Logon and Other Secure Screens (requires administrator privileges) button, and press Enter.

3. Answer Yes to the prompts regarding copying your settings and about copying plugins, and respond to the User Account Control prompt that may appear.
4. When settings are copied, press Enter to dismiss the OK button. Tab to OK and Enter once more to exit the dialog.

Once NVDA Remote is installed on the secure desktop, if you are currently being controlled in a remote session,
the secure desktop will read when switched to.

##Contributions
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
