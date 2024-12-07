import ctypes
import ctypes.wintypes
import logging
import os
import sys
import threading
from typing import Callable, Optional, Set, Tuple

import addonHandler
import api
import braille
import configobj
import core
import globalVars
import gui
import queueHandler
import speech
import ui
import wx
from config import isInstalledCopy
from globalPluginHandler import GlobalPlugin as _GlobalPlugin
from keyboardHandler import KeyboardInputGesture
from scriptHandler import script
from utils.security import isRunningOnSecureDesktop

from . import configuration, cues, local_machine, serializer, url_handler
from .alwaysCallAfter import alwaysCallAfter
from .connection_info import ConnectionInfo, ConnectionMode
from .menu import RemoteMenu
from .protocol import RemoteMessageType
from .secureDesktop import SecureDesktopHandler
from .session import MasterSession, SlaveSession
from .settings_panel import RemoteSettingsPanel
from .transport import RelayTransport
from logHandler import log
try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning(
		"Unable to initialise translations. This may be because the addon is running from NVDA scratchpad."
	)
from winUser import WM_QUIT  # provided by NVDA

from . import dialogs, keyboard_hook, server
from .socket_utils import addressToHostPort, hostPortToAddress

logging.getLogger("keyboard_hook").addHandler(logging.StreamHandler(sys.stdout))

# Type aliases
KeyModifier = Tuple[int, bool]  # (vk_code, extended)
Address = Tuple[str, int]  # (hostname, port) 



class GlobalPlugin(_GlobalPlugin):
	scriptCategory: str = _("NVDA Remote")
	localScripts: Set[Callable]
	localMachine: local_machine.LocalMachine
	masterSession: Optional[MasterSession] 
	slaveSession: Optional[SlaveSession]
	keyModifiers: Set[KeyModifier]
	hostPendingModifiers: Set[KeyModifier]
	connecting: bool
	masterTransport: Optional[RelayTransport]
	slaveTransport: Optional[RelayTransport]
	localControlServer: Optional[server.LocalRelayServer]
	hookThread: Optional[threading.Thread]
	sendingKeys: bool


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.keyModifiers = set()
		self.hostPendingModifiers = set()
		self.localScripts = {self.script_sendKeys}
		self.localMachine = local_machine.LocalMachine()
		self.slaveSession = None
		self.masterSession = None
		self.menu: RemoteMenu = RemoteMenu(self)
		self.connecting = False
		self.URLHandlerWindow = url_handler.URLHandlerWindow(callback=self.verifyConnect)
		url_handler.register_url_handler()
		self.masterTransport = None
		self.slaveTransport = None
		self.localControlServer = None
		self.hookThread = None
		self.sendingKeys = False
		try:
			configuration.get_config()
		except configobj.ParseError:
			os.remove(os.path.abspath(os.path.join(globalVars.appArgs.configPath, configuration.CONFIG_FILE_NAME)))
			queueHandler.queueFunction(queueHandler.eventQueue, wx.CallAfter, wx.MessageBox, _("Your NVDA Remote configuration was corrupted and has been reset."), _("NVDA Remote Configuration Error"), wx.OK|wx.ICON_EXCLAMATION)
		if not globalVars.appArgs.secure:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(RemoteSettingsPanel)
		self.sdHandler = SecureDesktopHandler()
		if isRunningOnSecureDesktop():
			connection = self.sdHandler.initialize_secure_desktop()
			if connection:
				self.connectAsSlave(connection.address, connection.channel, insecure=True)
				self.slaveSession.transport.connectedEvent.wait(self.sdHandler.SD_CONNECT_BLOCK_TIMEOUT)
		core.postNvdaStartup.register(self.performAutoconnect)

	def performAutoconnect(self):
		controlServerConfig = configuration.get_config()['controlserver']
		if not controlServerConfig['autoconnect'] or self.masterSession or self.slaveSession:
			log.debug("Autoconnect disabled or already connected")
			return
		key  = controlServerConfig['key']
		if controlServerConfig['self_hosted']:
			port = controlServerConfig['port']
			hostname = 'localhost'
			self.startControlServer(port, key )
		else:
			address = addressToHostPort(controlServerConfig['host'])
			hostname, port = address
		mode = ConnectionMode.SLAVE if controlServerConfig['connection_type']==0 else ConnectionMode.MASTER
		conInfo = ConnectionInfo(mode=mode, hostname=hostname, port=port, key=key)
		self.connect(conInfo)

	def terminate(self):
		self.sdHandler.terminate()
		self.disconnect()
		self.localMachine.terminate()
		self.localMachine = None
		self.menu.terminate()
		self.menu=None
		if not isInstalledCopy():
			url_handler.unregister_url_handler()
		self.URLHandlerWindow.destroy()
		self.URLHandlerWindow=None
		if not globalVars.appArgs.secure:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(RemoteSettingsPanel)


	def toggleMute(self):
		self.localMachine.isMuted = self.menu.muteItem.IsChecked()

	@script(description=_("""Mute or unmute the speech coming from the remote computer"""))
	def script_toggle_remote_mute(self, gesture):
		if not self.isConnected() or self.connecting: return
		self.localMachine.isMuted = not self.localMachine.isMuted
		self.menu.muteItem.Check(self.localMachine.isMuted)
		# Translators: Report when using gestures to mute or unmute the speech coming from the remote computer.
		status = _("Mute speech and sounds from the remote computer") if self.localMachine.isMuted else _("Unmute speech and sounds from the remote computer")
		ui.message(status)

	def pushClipboard(self):
		connector = self.slaveTransport or self.masterTransport
		try:
			connector.send(RemoteMessageType.set_clipboard_text, text=api.getClipData())
			cues.clipboard_pushed()
		except TypeError:
			log.exception("Unable to push clipboard")

	@script(gesture="kb:control+shift+NVDA+c", description=_("Sends the contents of the clipboard to the remote machine"))
	def script_push_clipboard(self, gesture):
		connector = self.slaveTransport or self.masterTransport
		if not getattr(connector,'connected',False):
			ui.message(_("Not connected."))
			return
		try:
			connector.send(RemoteMessageType.set_clipboard_text, text=api.getClipData())
			cues.clipboard_pushed()
			ui.message(_("Clipboard pushed"))
		except TypeError:
			ui.message(_("Unable to push clipboard"))

	def copyLink(self):
		session = self.masterSession or self.slaveSession
		url = session.getConnectionInfo().getURLToConnect()
		api.copyToClip(str(url))

	@script(description=_("""Copies a link to the remote session to the clipboard"""))
	def script_copy_link(self, gesture):
		self.copyLink()
		ui.message(_("Copied link"))

	def sendSAS(self):
		self.masterTransport.send(RemoteMessageType.send_SAS)

	def connect(self, connectionInfo: ConnectionInfo, insecure=False):
		if connectionInfo.mode == ConnectionMode.MASTER:
			self.connectAsMaster((connectionInfo.hostname, connectionInfo.port), connectionInfo.key, insecure)
		elif connectionInfo.mode == ConnectionMode.SLAVE:
			self.connectAsSlave((connectionInfo.hostname, connectionInfo.port), connectionInfo.key, insecure)

	def disconnect(self):
		if self.masterTransport is None and self.slaveTransport is None:
			return
		if self.localControlServer is not None:
			self.localControlServer.close()
			self.localControlServer = None
		if self.masterTransport is not None:
			self.disconnectAsMaster()
		if self.slaveTransport is not None:
			self.disconnectAsSlave()
		cues.disconnected()
		self.menu.handleConnected(False)

	def disconnectAsMaster(self):
		self.masterTransport.close()
		self.masterTransport = None
		self.masterSession = None

	def disconnectingAsMaster(self):
		if self.menu:
			self.menu.handleConnected(False)
		if self.localMachine:
			self.localMachine.isMuted = False
		self.sendingKeys = False
		if self.hookThread is not None:
			ctypes.windll.user32.PostThreadMessageW(self.hookThread.ident, WM_QUIT, 0, 0)
			self.hookThread.join()
			self.hookThread = None
		self.keyModifiers = set()

	def disconnectAsSlave(self):
		self.slaveTransport.close()
		self.slaveTransport = None
		self.slaveSession = None
		self.sdHandler.slave_session = None

	@alwaysCallAfter
	def onConnectAsMasterFailed(self):
		if self.masterTransport.successfulConnects == 0:
			self.disconnectAsMaster()
			# Translators: Title of the connection error dialog.
			gui.messageBox(parent=gui.mainFrame, caption=_("Error Connecting"),
			# Translators: Message shown when cannot connect to the remote computer.
			message=_("Unable to connect to the remote computer"), style=wx.OK | wx.ICON_WARNING)

	@script(gesture="kb:alt+NVDA+pageDown", description=_("""Disconnect a remote session"""))
	def script_disconnect(self, gesture):
		if not self.isConnected:
			ui.message(_("Not connected."))
			return
		self.disconnect()

	@script(gesture="kb:alt+NVDA+pageUp", description=_("""Connect to a remote computer"""))
	def script_connect(self, gesture):
		if self.isConnected() or self.connecting:
			return
		self.doConnect(evt = None)

	def doConnect(self, evt=None):
		if evt is not None:
			evt.Skip()
		previousConnections = configuration.get_config()['connections']['last_connected']
		hostnames = list(reversed(previousConnections))
		# Translators: Title of the connect dialog.
		dlg = dialogs.DirectConnectDialog(parent=gui.mainFrame, id=wx.ID_ANY, title=_("Connect"), hostnames=hostnames)
		
		def handleDialogCompletion(dlg_result):
			if dlg_result != wx.ID_OK:
				return
			connectionInfo = dlg.getConnectionInfo()
			if dlg.client_or_server.GetSelection() == 1:  # server
				self.startControlServer(connectionInfo.port, connectionInfo.key)
			self.connect(connectionInfo=connectionInfo, insecure=dlg.client_or_server.GetSelection() == 1)
		gui.runScriptModalDialog(dlg, callback=handleDialogCompletion)

	def onConnectedAsMaster(self):
		configuration.write_connection_to_config(self.masterTransport.address)
		self.menu.handleConnected(True)
		# We might have already created a hook thread before if we're restoring an
		# interrupted connection. We must not create another.
		if not self.hookThread:
			self.hookThread = threading.Thread(target=self.hook)
			self.hookThread.daemon = True
			self.hookThread.start()
		# Translators: Presented when connected to the remote computer.
		ui.message(_("Connected!"))
		cues.connected()

	def onDisconnectedAsMaster(self):
		# Translators: Presented when connection to a remote computer was interupted.
		ui.message(_("Connection interrupted"))

	def connectAsMaster(self, address, key, insecure=False):
		transport = RelayTransport(address=address, serializer=serializer.JSONSerializer(), channel=key, connection_type='master', insecure=insecure)
		self.masterSession = MasterSession(transport=transport, localMachine=self.localMachine)
		transport.transportCertificateAuthenticationFailed.register(self.onMasterCertificateFailed)
		transport.transportConnected.register(self.onConnectedAsMaster)
		transport.transportConnectionFailed.register(self.onConnectAsMasterFailed)
		transport.transportClosing.register(self.disconnectingAsMaster)
		transport.transportDisconnected.register(self.onDisconnectedAsMaster)
		transport.reconnectorThread.start()
		self.masterTransport = transport

	def connectAsSlave(self, address, key, insecure=False):
		transport = RelayTransport(serializer=serializer.JSONSerializer(), address=address, channel=key, connection_type='slave', insecure=insecure)
		self.slaveSession = SlaveSession(transport=transport, localMachine=self.localMachine)
		self.sdHandler.slave_session = self.slaveSession
		self.slaveTransport = transport
		transport.transportCertificateAuthenticationFailed.register(self.onSlaveCertificateFailed)
		transport.transportConnected.register(self.on_connected_as_slave)
		transport.reconnectorThread.start()
		self.menu.disconnectItem.Enable(True)
		self.menu.connectItem.Enable(False)

	def handleCertificateFailure(self, transport: RelayTransport):
		self.last_fail_address = transport.address
		self.last_fail_key = transport.channel
		self.disconnect()
		try:
			cert_hash = transport.lastFailFingerprint

			wnd = dialogs.CertificateUnauthorizedDialog(None, fingerprint=cert_hash)
			a = wnd.ShowModal()
			if a == wx.ID_YES:
				config = configuration.get_config()
				config['trusted_certs'][hostPortToAddress(self.last_fail_address)]=cert_hash
				config.write()
			if a == wx.ID_YES or a == wx.ID_NO: return True
		except Exception as ex:
			log.error(ex)
		return False

	@alwaysCallAfter
	def onMasterCertificateFailed(self):
		if self.handleCertificateFailure(self.masterTransport):
			self.connectAsMaster(self.last_fail_address, self.last_fail_key, True)

	@alwaysCallAfter
	def onSlaveCertificateFailed(self):
		if self.handleCertificateFailure(self.slaveTransport):
			self.connectAsSlave(self.last_fail_address, self.last_fail_key, True)

	@alwaysCallAfter
	def on_connected_as_slave(self):
		log.info("Control connector connected")
		cues.control_server_connected()
		# Translators: Presented in direct (client to server) remote connection when the controlled computer is ready.
		speech.speakMessage(_("Connected to control server"))
		self.menu.pushClipboardItem.Enable(True)
		self.menu.copyLinkItem.Enable(True)
		configuration.write_connection_to_config(self.slaveTransport.address)

	def startControlServer(self, server_port, channel):
		self.localControlServer = server.LocalRelayServer(server_port, channel)
		serverThread = threading.Thread(target=self.localControlServer.run)
		serverThread.daemon = True
		serverThread.start()

	def hook(self):
		log.debug("Hook thread start")
		keyhook = keyboard_hook.KeyboardHook()
		keyhook.register_callback(self.hook_callback)
		msg = ctypes.wintypes.MSG()
		while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), None, 0, 0):
			pass
		log.debug("Hook thread end")
		keyhook.free()

	def hook_callback(self, **kwargs):
		if not self.sendingKeys:
			return False
		keyCode = (kwargs['vk_code'], kwargs['extended'])
		gesture = KeyboardInputGesture(self.keyModifiers, keyCode[0], kwargs['scan_code'], keyCode[1])
		if not kwargs['pressed'] and keyCode in self.hostPendingModifiers:
			self.hostPendingModifiers.discard(keyCode)
			return False
		gesture = KeyboardInputGesture(self.keyModifiers, keyCode[0], kwargs['scan_code'], keyCode[1])
		if gesture.isModifier:
			if kwargs['pressed']:
				self.keyModifiers.add(keyCode)
			else:
				self.keyModifiers.discard(keyCode)
		elif kwargs['pressed']:
			script = gesture.script
			if script in self.localScripts:
				wx.CallAfter(script, gesture)
				return True
		self.masterTransport.send(RemoteMessageType.key, **kwargs)
		return True #Don't pass it on

	@script(
		# Translators: Documentation string for the script that toggles the control between guest and host machine.
		description=_("Toggles the control between guest and host machine"),
		gesture="kb:f11",
		)
	def script_sendKeys(self, gesture):
		if not self.masterTransport:
			gesture.send()
			return
		self.sendingKeys = not self.sendingKeys
		self.setReceivingBraille(self.sendingKeys)
		if self.sendingKeys:
			self.hostPendingModifiers = gesture.modifiers
			# Translators: Presented when sending keyboard keys from the controlling computer to the controlled computer.
			ui.message(_("Controlling remote machine."))
		else:
			self.releaseKeys()
			# Translators: Presented when keyboard control is back to the controlling computer.
			ui.message(_("Controlling local machine."))

	def releaseKeys(self):
		# release all pressed keys in the guest.
		for k in self.keyModifiers:
			self.masterTransport.send(RemoteMessageType.key, vk_code=k[0], extended=k[1], pressed=False)
		self.keyModifiers = set()

	def setReceivingBraille(self, state):
		if state and self.masterSession.patchCallbacksAdded and braille.handler.enabled:
			self.masterSession.patcher.registerBrailleInput()
			self.localMachine.receivingBraille=True
		elif not state:
			self.masterSession.patcher.unregisterBrailleInput()
			self.localMachine.receivingBraille=False

	@alwaysCallAfter
	def verifyConnect(self, conInfo: ConnectionInfo):
		if self.isConnected() or self.connecting:
			gui.messageBox(_("NVDA Remote is already connected. Disconnect before opening a new connection."), _("NVDA Remote Already Connected"), wx.OK|wx.ICON_WARNING)
			return
		self.connecting = True
		serverAddr = conInfo.getAddress()
		key = conInfo.key
		if conInfo.mode == ConnectionMode.MASTER:
			question = _("Do you wish to control the machine on server {server} with key {key}?").format(server=serverAddr, key=key)
		elif conInfo.mode == ConnectionMode.SLAVE:
			question = _("Do you wish to allow this machine to be controlled on server {server} with key {key}?").format(server=serverAddr, key=key)
		if gui.messageBox(question, _("NVDA Remote Connection Request"), wx.YES|wx.NO|wx.NO_DEFAULT|wx.ICON_WARNING) != wx.YES:
			self.connecting = False
			return
		self.connect(conInfo)
		self.connecting = False

	def isConnected(self):
		connector = self.slaveTransport or self.masterTransport
		if connector is not None:
			return connector.connected
		return False
