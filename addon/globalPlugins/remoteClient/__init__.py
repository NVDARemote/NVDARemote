import logging

from typing import Optional, Set, Dict, List, Any, Callable, Union, Type, Tuple

from .secureDesktop import SecureDesktopHandler

from .menu import RemoteMenu

# Type aliases
KeyModifier = Tuple[int, bool]  # (vk_code, extended)
Address = Tuple[str, int]  # (hostname, port) 

logger = logging.getLogger(__name__)

import ctypes
import ctypes.wintypes
import json
import os
import socket
import ssl
import sys
import threading
import uuid

import addonHandler
import api
import braille
import configobj
import globalVars
import gui
import IAccessibleHandler
import speech
import ui
import wx
from config import isInstalledCopy
from globalPluginHandler import GlobalPlugin as _GlobalPlugin
from keyboardHandler import KeyboardInputGesture
from scriptHandler import script
from utils.security import isRunningOnSecureDesktop

from . import configuration, cues, local_machine, serializer, url_handler
from .session import MasterSession, SlaveSession
from .transport import RelayTransport, TransportEvents

try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	from logHandler import log
	log.warning(
		"Unable to initialise translations. This may be because the addon is running from NVDA scratchpad."
	)
from winUser import WM_QUIT  # provided by NVDA

from . import bridge, dialogs, keyboard_hook, server
from .socket_utils import SERVER_PORT, address_to_hostport, hostport_to_address

logging.getLogger("keyboard_hook").addHandler(logging.StreamHandler(sys.stdout))
import queueHandler
import shlobj
from logHandler import log

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
		self.url_handler_window = url_handler.URLHandlerWindow(callback=self.verifyConnect)
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
		controlServerConfig = configuration.get_config()['controlserver']
		self.sd_handler = SecureDesktopHandler()
		if isRunningOnSecureDesktop():
			connection = self.sd_handler.initialize_secure_desktop()
			if connection:
				self.connectAsSlave(connection.address, connection.channel, insecure=True)
		if controlServerConfig['autoconnect'] and not self.masterSession and not self.slaveSession:
			self.performAutoconnect()

	def performAutoconnect(self):
		controlServerConfig = configuration.get_config()['controlserver']
		channel = controlServerConfig['key']
		if controlServerConfig['self_hosted']:
			port = controlServerConfig['port']
			address = ('localhost',port)
			self.startControlServer(port, channel)
		else:
			address = address_to_hostport(controlServerConfig['host'])
		if controlServerConfig['connection_type']==0:
			self.connectAsSlave(address, channel)
		else:
			self.connectAsMaster(address, channel)


	def terminate(self):
		self.sd_handler.terminate()
		self.disconnect()
		self.localMachine.terminate()
		self.localMachine = None
		self.menu.terminate()
		self.menu=None
		if not isInstalledCopy():
			url_handler.unregister_url_handler()
		self.url_handler_window.destroy()
		self.url_handler_window=None

	def toggleMute(self):
		self.localMachine.isMuted = self.menu.muteItem.IsChecked()

	def script_toggle_remote_mute(self, gesture):
		if not self.is_connected() or self.connecting: return
		self.localMachine.isMuted = not self.localMachine.isMuted
		self.menu.muteItem.Check(self.localMachine.isMuted)
		# Translators: Report when using gestures to mute or unmute the speech coming from the remote computer.
		status = _("Mute speech and sounds from the remote computer") if self.localMachine.isMuted else _("Unmute speech and sounds from the remote computer")
		ui.message(status)
	script_toggle_remote_mute.__doc__ = _("""Mute or unmute the speech coming from the remote computer""")

	def pushClipboard(self):
		connector = self.slaveTransport or self.masterTransport
		try:
			connector.send(type='set_clipboard_text', text=api.getClipData())
			cues.clipboard_pushed()
		except TypeError:
			log.exception("Unable to push clipboard")

	def script_push_clipboard(self, gesture):
		connector = self.slaveTransport or self.masterTransport
		if not getattr(connector,'connected',False):
			ui.message(_("Not connected."))
			return
		try:
			connector.send(type='set_clipboard_text', text=api.getClipData())
			cues.clipboard_pushed()
			ui.message(_("Clipboard pushed"))
		except TypeError:
			ui.message(_("Unable to push clipboard"))
	script_push_clipboard.__doc__ = _("Sends the contents of the clipboard to the remote machine")

	def copyLink(self):
		session = self.masterSession or self.slaveSession
		url = session.getConnectionInfo().get_url_to_connect()
		api.copyToClip(str(url))

	def script_copy_link(self, gesture):
		self.copyLink()
		ui.message(_("Copied link"))
	script_copy_link.__doc__ = _("Copies a link to the remote session to the clipboard")

	def displayOptionsInterface(self):
		conf = configuration.get_config()
		# Translators: The title of the add-on options dialog.
		dlg = dialogs.OptionsDialog(gui.mainFrame, wx.ID_ANY, title=_("Options"))
		dlg.set_from_config(conf)
		def handle_dlg_complete(dlg_result):
			if dlg_result != wx.ID_OK:
				return
			dlg.write_to_config(conf)
		gui.runScriptModalDialog(dlg, callback=handle_dlg_complete)

	def sendSAS(self):
		self.masterTransport.send('send_SAS')

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
			self.menu.muteItem.Check(False)
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
		self.sd_handler.slave_session = None

	def on_connected_as_master_failed(self):
		if self.masterTransport.successful_connects == 0:
			self.disconnectAsMaster()
			# Translators: Title of the connection error dialog.
			gui.messageBox(parent=gui.mainFrame, caption=_("Error Connecting"),
			# Translators: Message shown when cannot connect to the remote computer.
			message=_("Unable to connect to the remote computer"), style=wx.OK | wx.ICON_WARNING)

	def script_disconnect(self, gesture):
		if self.masterTransport is None and self.slaveTransport is None:
			ui.message(_("Not connected."))
			return
		self.disconnect()
	script_disconnect.__doc__ = _("""Disconnect a remote session""")

	def script_connect(self, gesture):
		if self.is_connected() or self.connecting: return
		self.doConnect(evt = None)
	script_connect.__doc__ = _("""Connect to a remote computer""")
	
	def doConnect(self, evt):
		if evt is not None: evt.Skip()
		previousConnections = configuration.get_config()['connections']['last_connected']
		# Translators: Title of the connect dialog.
		dlg = dialogs.DirectConnectDialog(parent=gui.mainFrame, id=wx.ID_ANY, title=_("Connect"))
		dlg.panel.host.SetItems(list(reversed(previousConnections)))
		dlg.panel.host.SetSelection(0)
		def handle_dlg_complete(dlg_result):
			if dlg_result != wx.ID_OK:
				return
			if dlg.client_or_server.GetSelection() == 0: #client
				host = dlg.panel.host.GetValue()
				server_addr, port = address_to_hostport(host)
				channel = dlg.getKey()
				if dlg.connection_type.GetSelection() == 0:
					self.connectAsMaster((server_addr, port), channel)
				else:
					self.connectAsSlave((server_addr, port), channel)
			else: #We want a server
				channel = dlg.getKey()
				self.startControlServer(int(dlg.panel.port.GetValue()), channel)
				if dlg.connection_type.GetSelection() == 0:
					self.connectAsMaster(('127.0.0.1', int(dlg.panel.port.GetValue())), channel, insecure=True)
				else:
					self.connectAsSlave(('127.0.0.1', int(dlg.panel.port.GetValue())), channel, insecure=True)
		gui.runScriptModalDialog(dlg, callback=handle_dlg_complete)

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
		self.masterSession = MasterSession(transport=transport, local_machine=self.localMachine)
		transport.callback_manager.registerCallback(TransportEvents.CERTIFICATE_AUTHENTICATION_FAILED, self.on_certificate_as_master_failed)
		transport.callback_manager.registerCallback(TransportEvents.CONNECTED, self.onConnectedAsMaster)
		transport.callback_manager.registerCallback(TransportEvents.CONNECTION_FAILED, self.on_connected_as_master_failed)
		transport.callback_manager.registerCallback(TransportEvents.CLOSING, self.disconnectingAsMaster)
		transport.callback_manager.registerCallback(TransportEvents.DISCONNECTED, self.onDisconnectedAsMaster)
		self.masterTransport = transport
		self.masterTransport.reconnector_thread.start()

	def connectAsSlave(self, address, key, insecure=False):
		transport = RelayTransport(serializer=serializer.JSONSerializer(), address=address, channel=key, connection_type='slave', insecure=insecure)
		self.slaveSession = SlaveSession(transport=transport, local_machine=self.localMachine)
		self.sd_handler.slave_session = self.slaveSession
		self.slaveTransport = transport
		transport.callback_manager.registerCallback(TransportEvents.CERTIFICATE_AUTHENTICATION_FAILED, self.on_certificate_as_slave_failed)
		self.slaveTransport.callback_manager.registerCallback(TransportEvents.CONNECTED, self.on_connected_as_slave)
		self.slaveTransport.reconnector_thread.start()
		self.menu.disconnectItem.Enable(True)
		self.menu.connectItem.Enable(False)

	def handle_certificate_failed(self, transport):
		self.last_fail_address = transport.address
		self.last_fail_key = transport.channel
		self.disconnect()
		try:
			cert_hash = transport.last_fail_fingerprint

			wnd = dialogs.CertificateUnauthorizedDialog(None, fingerprint=cert_hash)
			a = wnd.ShowModal()
			if a == wx.ID_YES:
				config = configuration.get_config()
				config['trusted_certs'][hostport_to_address(self.last_fail_address)]=cert_hash
				config.write()
			if a == wx.ID_YES or a == wx.ID_NO: return True
		except Exception as ex:
			log.error(ex)
		return False

	def on_certificate_as_master_failed(self):
		if self.handle_certificate_failed(self.masterTransport):
			self.connectAsMaster(self.last_fail_address, self.last_fail_key, True)

	def on_certificate_as_slave_failed(self):
		if self.handle_certificate_failed(self.slaveTransport):
			self.connectAsSlave(self.last_fail_address, self.last_fail_key, True)

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
		self.masterTransport.send(type="key", **kwargs)
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
			self.masterTransport.send(type="key", vk_code=k[0], extended=k[1], pressed=False)
		self.keyModifiers = set()

	def setReceivingBraille(self, state):
		if state and self.masterSession.patchCallbacksAdded and braille.handler.enabled:
			self.masterSession.patcher.patchBrailleInput()
			self.localMachine.receivingBraille=True
		elif not state:
			self.masterSession.patcher.unpatchBrailleInput()
			self.localMachine.receivingBraille=False

	def verifyConnect(self, con_info):
		if self.is_connected() or self.connecting:
			gui.messageBox(_("NVDA Remote is already connected. Disconnect before opening a new connection."), _("NVDA Remote Already Connected"), wx.OK|wx.ICON_WARNING)
			return
		self.connecting = True
		server_addr = con_info.get_address()
		key = con_info.key
		if con_info.mode == 'master':
			message = _("Do you wish to control the machine on server {server} with key {key}?").format(server=server_addr, key=key)
		elif con_info.mode == 'slave':
			message = _("Do you wish to allow this machine to be controlled on server {server} with key {key}?").format(server=server_addr, key=key)
		if gui.messageBox(message, _("NVDA Remote Connection Request"), wx.YES|wx.NO|wx.NO_DEFAULT|wx.ICON_WARNING) != wx.YES:
			self.connecting = False
			return
		if con_info.mode == 'master':
			self.connectAsMaster((con_info.hostname, con_info.port), key=key)
		elif con_info.mode == 'slave':
			self.connectAsSlave((con_info.hostname, con_info.port), key=key)
		self.connecting = False

	def is_connected(self):
		connector = self.slaveTransport or self.masterTransport
		if connector is not None:
			return connector.connected
		return False

	__gestures = {
		"kb:alt+NVDA+pageDown": "disconnect",
		"kb:alt+NVDA+pageUp": "connect",
		"kb:control+shift+NVDA+c": "push_clipboard",
	}
