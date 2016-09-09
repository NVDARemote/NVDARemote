SERVER_ADDR = ('127.0.0.1', 5000)
CONFIG_FILE_NAME = 'remote.ini'
from cStringIO import StringIO
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import json
sys.path.remove(sys.path[-1])
import threading
import time
import socket
from globalPluginHandler import GlobalPlugin
import logging
logger = logging.getLogger(__name__)
import Queue
import select
import config
import configobj
import validate
import wx
import gui
import beep_sequence
import speech
from transport import RelayTransport, ConnectorThread
import local_machine
import serializer
from session import MasterSession, SlaveSession
import time
import ui
import addonHandler
addonHandler.initTranslation()
import keyboard_hook
import ctypes.wintypes as ctypes
import win32con
logging.getLogger("keyboard_hook").addHandler(logging.StreamHandler(sys.stdout))
from logHandler import log
import dialogs
import IAccessibleHandler
import tones
import globalVars
import shlobj
import uuid
import server
import bridge
from socket_utils import SERVER_PORT, address_to_hostport, hostport_to_address
import api
import ssl

class GlobalPlugin(GlobalPlugin):
	scriptCategory = _("NVDA Remote")

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		self.local_machine = local_machine.LocalMachine()
		self.slave_session = None
		self.master_session = None
		self.create_menu()
		self.connector = None
		self.control_connector_thread = None
		self.control_connector = None
		self.server = None
		self.hook_thread = None
		self.sending_keys = False
		self.key_modified = False
		self.sd_server = None
		cs = get_config()['controlserver']
		self.temp_location = os.path.join(shlobj.SHGetFolderPath(0, shlobj.CSIDL_COMMON_APPDATA), 'temp')
		self.ipc_file = os.path.join(self.temp_location, 'remote.ipc')
		if not self.check_secure_desktop() and cs['autoconnect']:
			self.perform_autoconnect()
		self.sd_focused = False

	def perform_autoconnect(self):
		cs = get_config()['controlserver']
		channel = cs['key']
		if cs['self_hosted']:
			address = address_to_hostport('localhost')
			self.start_control_server(address[1], channel)
		else:
			address = address_to_hostport(cs['host'])
		self.connect_control(address, channel)

	def create_menu(self):
		self.menu = wx.Menu()
		tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
		# Translators: Item in NVDA Remote submenu to connect to a remote computer.
		self.connect_item = self.menu.Append(wx.ID_ANY, _("Connect..."), _("Remotely connect to another computer running NVDA Remote Access"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.do_connect, self.connect_item)
		# Translators: Item in NVDA Remote submenu to disconnect from a remote computer.
		self.disconnect_item = self.menu.Append(wx.ID_ANY, _("Disconnect"), _("Disconnect from another computer running NVDA Remote Access"))
		self.disconnect_item.Enable(False)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.on_disconnect_item, self.disconnect_item)
		# Translators: Menu item in NvDA Remote submenu to mute speech and sounds from the remote computer.
		self.mute_item = self.menu.Append(wx.ID_ANY, _("Mute remote"), _("Mute speech and sounds from the remote computer"))
		self.mute_item.SetCheckable(True)
		self.mute_item.Enable(False)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.on_mute_item, self.mute_item)
		# Translators: Menu item in NVDA Remote submenu to push clipboard content to the remote computer.
		self.push_clipboard_item = self.menu.Append(wx.ID_ANY, _("&Push clipboard"), _("Push the clipboard to the other machine"))
		self.push_clipboard_item.Enable(False)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.on_push_clipboard_item, self.push_clipboard_item)
		# Translators: Menu item in NvDA Remote submenu to open add-on options.
		self.options_item = self.menu.Append(wx.ID_ANY, _("&Options..."), _("Options"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.on_options_item, self.options_item)
		# Translators: Menu item in NVDA Remote submenu to send Control+Alt+Delete to the remote computer.
		self.send_ctrl_alt_del_item = self.menu.Append(wx.ID_ANY, _("Send Ctrl+Alt+Del"), _("Send Ctrl+Alt+Del"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.on_send_ctrl_alt_del, self.send_ctrl_alt_del_item)
		self.send_ctrl_alt_del_item.Enable(False)
		# Translators: Label of menu in NVDA tools menu.
		self.remote_item=tools_menu.AppendSubMenu(self.menu, _("R&emote"), _("NVDA Remote Access"))

	def terminate(self):
		self.do_disconnect_from_slave(True)
		self.local_machine = None
		self.menu.RemoveItem(self.connect_item)
		self.connect_item.Destroy()
		self.connect_item=None
		self.menu.RemoveItem(self.disconnect_item)
		self.disconnect_item.Destroy()
		self.disconnect_item=None
		self.menu.RemoveItem(self.mute_item)
		self.mute_item.Destroy()
		self.mute_item=None
		self.menu.RemoveItem(self.push_clipboard_item)
		self.push_clipboard_item.Destroy()
		self.push_clipboard_item=None
		self.menu.RemoveItem(self.options_item)
		self.options_item.Destroy()
		self.options_item=None
		self.menu.RemoveItem(self.send_ctrl_alt_del_item)
		self.send_ctrl_alt_del_item.Destroy()
		self.send_ctrl_alt_del_item=None
		tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
		tools_menu.RemoveItem(self.remote_item)
		self.remote_item.Destroy()
		self.remote_item=None
		try:
			self.menu.Destroy()
		except wx.PyDeadObjectError:
			pass
		try:
			os.unlink(self.ipc_file)
		except:
			pass
		self.menu=None

	def on_disconnect_item(self, evt):
		evt.Skip()
		self.do_disconnect_from_slave()

	def on_mute_item(self, evt):
		evt.Skip()
		self.local_machine.is_muted = self.mute_item.IsChecked()

	def script_toggle_remote_mute(self, gesture):
		self.local_machine.is_muted = not self.local_machine.is_muted
		self.mute_item.Check(self.local_machine.is_muted)
	script_toggle_remote_mute.__doc__ = _("""Mute or unmute the speech coming from the remote computer""")

	def on_push_clipboard_item(self, evt):
		connector = self.control_connector or self.connector
		try:
			connector.send(type='set_clipboard_text', text=api.getClipData())
		except TypeError:
			# JL: It might be helpful to provide a log.debug output for this.
			pass

	def on_options_item(self, evt):
		evt.Skip()
		config = get_config()
		# Translators: The title of the add-on options dialog.
		dlg = dialogs.OptionsDialog(gui.mainFrame, wx.ID_ANY, title=_("Options"))
		dlg.set_from_config(config)
		def handle_dlg_complete(dlg_result):
			if dlg_result != wx.ID_OK:
				return
			dlg.write_to_config(config)
		gui.runScriptModalDialog(dlg, callback=handle_dlg_complete)

	def on_send_ctrl_alt_del(self, evt):
		self.connector.send('send_SAS')

	def do_disconnect_from_slave(self, quiet=False):
		if self.connector is None and self.control_connector is None:
			if not quiet:
				ui.message(_("Not connected."))
			return
		if self.connector is not None:
			self.disconnect_from_slave()
		if self.control_connector is not None:
			self.disconnect_control()
		if self.server is not None:
			self.server.close()
			self.server = None
		beep_sequence.beep_sequence((660, 60), (440, 60))
		self.disconnect_item.Enable(False)
		self.connect_item.Enable(True)
		self.push_clipboard_item.Enable(False)

	def disconnect_from_slave(self):
		self.connector.close()
		self.connector = None
		if self.connector_thread is not None:
			self.connector_thread.running = False
		self.connect_item.Enable(True)
		self.disconnect_item.Enable(False)
		self.mute_item.Check(False)
		self.mute_item.Enable(False)
		self.push_clipboard_item.Enable(False)
		self.send_ctrl_alt_del_item.Enable(False)
		self.sending_keys = False
		if self.hook_thread is not None:
			ctypes.windll.user32.PostThreadMessageW(self.hook_thread.ident, win32con.WM_QUIT, 0, 0)
			self.hook_thread.join()
			self.hook_thread = None
		self.key_modified = False

	def disconnect_control(self):
		self.control_connector_thread.running = False
		self.control_connector.close()
		self.control_connector = None

	def on_slave_connection_failed(self):
		if self.connector.successful_connects == 0:
			self.disconnect_from_slave()
			# Translators: Title of the connection error dialog.
			gui.messageBox(parent=gui.mainFrame, caption=_("Error Connecting"),
			# Translators: Message shown when cannot connect to the remote computer.
			message=_("Unable to connect to the remote computer"), style=wx.OK | wx.ICON_WARNING)

	def script_disconnect(self, gesture):
		self.do_disconnect_from_slave()
	script_disconnect.__doc__ = _("""Disconnect a remote session""")

	def do_connect(self, evt):
		evt.Skip()
		last_cons = get_config()['connections']['last_connected']
		last = ''
		if last_cons:
			last = last_cons[-1]
		# Translators: Title of the connect dialog.
		dlg = dialogs.DirectConnectDialog(parent=gui.mainFrame, id=wx.ID_ANY, title=_("Connect"))
		dlg.panel.host.SetValue(last)
		dlg.panel.host.SelectAll()
		def handle_dlg_complete(dlg_result):
			if dlg_result != wx.ID_OK:
				return
			if dlg.client_or_server.GetSelection() == 0: #client
				server_addr = dlg.panel.host.GetValue()
				server_addr, port = address_to_hostport(server_addr)
				channel = dlg.panel.key.GetValue()
				if dlg.connection_type.GetSelection() == 0:
					self.connect_slave((server_addr, port), channel)
				else:
					self.connect_control((server_addr, port), channel)
			else: #We want a server
				channel = dlg.panel.key.GetValue()
				self.start_control_server(SERVER_PORT, channel)
				if dlg.connection_type.GetSelection() == 0:
					self.connect_slave(('127.0.0.1', SERVER_PORT), channel)
				else:
					self.connect_control(('127.0.0.1', SERVER_PORT), channel)
		gui.runScriptModalDialog(dlg, callback=handle_dlg_complete)

	def on_connected_to_slave(self):
		write_connection_to_config(self.connector.address)
		self.disconnect_item.Enable(True)
		self.connect_item.Enable(False)
		self.mute_item.Enable(True)
		self.push_clipboard_item.Enable(True)
		self.send_ctrl_alt_del_item.Enable(True)
		self.hook_thread = threading.Thread(target=self.hook)
		self.hook_thread.daemon = True
		self.hook_thread.start()
		# Translators: Presented when connected to the remote computer.
		ui.message(_("Connected!"))
		beep_sequence.beep_sequence((440, 60), (660, 60))

	def on_disconnected_from_slave(self):
		# Translators: Presented when connection to a remote computer was interupted.
		ui.message(_("Connection interrupted"))

	def connect_slave(self, address, channel):
		transport = RelayTransport(address=address, serializer=serializer.JSONSerializer(), channel=channel)
		self.master_session = MasterSession(transport=transport, local_machine=self.local_machine)
		transport.callback_manager.register_callback('transport_connected', self.on_connected_to_slave)
		transport.callback_manager.register_callback('transport_connection_failed', self.on_slave_connection_failed)
		transport.callback_manager.register_callback('transport_disconnected', self.on_disconnected_from_slave)
		self.connector = transport
		self.connector_thread = ConnectorThread(connector=transport)
		self.connector_thread.start()

	def connect_control(self, address=SERVER_ADDR, key=None):
		if self.control_connector_thread is not None:
			self.control_connector_thread.running = False
			if self.control_connector is not None:
				self.control_connector.close()
			self.control_connector_thread = None

		transport = RelayTransport(serializer=serializer.JSONSerializer(), address=address, channel=key)
		self.slave_session = SlaveSession(transport=transport, local_machine=self.local_machine)
		self.control_connector = transport
		self.control_connector.callback_manager.register_callback('transport_connected', self.connected_to_relay)
		self.control_connector_thread = ConnectorThread(connector=self.control_connector)
		self.control_connector_thread.start()
		self.disconnect_item.Enable(True)
		self.connect_item.Enable(False)

	def connected_to_relay(self):
		log.info("Control connector connected")
		beep_sequence.beep_sequence((720, 100), 50, (720, 100), 50, (720, 100))
		# Transaltors: Presented in direct (client to server) remote connection when the controlled computer is ready.
		speech.speakMessage(_("Connected to control server"))
		self.push_clipboard_item.Enable(True)
		write_connection_to_config(self.control_connector.address)

	def start_control_server(self, server_port, channel):
		self.server = server.Server(server_port, channel)
		server_thread = threading.Thread(target=self.server.run)
		server_thread.daemon = True
		server_thread.start()

	def hook(self):
		log.debug("Hook thread start")
		keyhook = keyboard_hook.KeyboardHook()
		keyhook.register_callback(self.hook_callback)
		msg = ctypes.MSG()
		while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), None, 0, 0):
			pass
		log.debug("Hook thread end")
		keyhook.free()

	def hook_callback(self, **kwargs):
		if kwargs['vk_code'] != win32con.VK_F11:
			self.key_modified = kwargs['pressed']
		if kwargs['vk_code'] == win32con.VK_F11 and kwargs['pressed'] and not self.key_modified:
			self.sending_keys = not self.sending_keys
			if self.sending_keys:
				# Translators: Presented when sending keyboard keys from the controlling computer to the controlled computer.
				ui.message(_("Sending keys."))
			else:
				# Translators: Presented when keyboard control is back to the controlling computer.
				ui.message(_("Not sending keys."))
			return True #Don't pass it on
		if not self.sending_keys:
			return False #Let the host have it
		self.connector.send(type="key", **kwargs)
		return True #Don't pass it on

	def event_gainFocus(self, obj, nextHandler):
		if isinstance(obj, IAccessibleHandler.SecureDesktopNVDAObject):
			self.sd_focused = True
			self.enter_secure_desktop()
		elif self.sd_focused and not isinstance(obj, IAccessibleHandler.SecureDesktopNVDAObject):
			#event_leaveFocus won't work for some reason
			self.sd_focused = False
			self.leave_secure_desktop()
		nextHandler()

	def enter_secure_desktop(self):
		"""function ran when entering a secure desktop."""
		if self.control_connector is None:
			return
		if not os.path.exists(self.temp_location):
			os.makedirs(self.temp_location)
		channel = str(uuid.uuid4())
		self.sd_server = server.Server(port=0, password=channel, bind_host='127.0.0.1')
		port = self.sd_server.server_socket.getsockname()[1]
		server_thread = threading.Thread(target=self.sd_server.run)
		server_thread.daemon = True
		server_thread.start()
		self.sd_relay = RelayTransport(address=('127.0.0.1', port), serializer=serializer.JSONSerializer(), channel=channel)
		self.sd_bridge = bridge.BridgeTransport(self.control_connector, self.sd_relay)
		relay_thread = threading.Thread(target=self.sd_relay.run)
		relay_thread.daemon = True
		relay_thread.start()
		data = [port, channel]
		with open(self.ipc_file, 'wb') as fp:
			json.dump(data, fp)

	def leave_secure_desktop(self):
		if self.sd_server is None:
			return #Nothing to do
		self.sd_bridge.disconnect()
		self.sd_server.close()
		self.sd_relay.close()

	def check_secure_desktop(self):
		if not globalVars.appArgs.secure:
			return False
		try:
			with open(self.ipc_file) as fp:
				data = json.load(fp)
			os.unlink(self.ipc_file)
			port, channel = data
			test_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			test_socket=ssl.wrap_socket(test_socket)
			test_socket.connect(('127.0.0.1', port))
			test_socket.close()
			self.connect_control(('127.0.0.1', port), channel)
			return True
		except:
			return False

	__gestures = {
		"kb:alt+NVDA+pageDown": "disconnect",
	}


_config = None
configspec = StringIO("""[connections]
last_connected = list(default=list())
[controlserver]
autoconnect = boolean(default=False)
self_hosted = boolean(default=False)
host = string(default="")
key = string(default="")
""")
def get_config():
	global _config
	if not _config:
		path = os.path.join(globalVars.appArgs.configPath, CONFIG_FILE_NAME)
		_config = configobj.ConfigObj(path, configspec=configspec)
		val = validate.Validator()
		_config.validate(val, copy=True)
	return _config

def write_connection_to_config(address):
	"""Writes an address to the last connected section of the config.
	If the address is already in the config, move it to the end."""
	conf = get_config()
	last_cons = conf['connections']['last_connected']
	address = hostport_to_address(address)
	if address in last_cons:
		conf['connections']['last_connected'].remove(address)
	conf['connections']['last_connected'].append(address)
	conf.write()
