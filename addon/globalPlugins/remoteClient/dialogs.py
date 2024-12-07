import json
import random
import threading
from typing import Any, Dict, Optional, Union, cast
from urllib import request

import addonHandler
import gui
import wx
from logHandler import log

from . import configuration, serializer, server, socket_utils, transport
from .alwaysCallAfter import alwaysCallAfter
from .connection_info import ConnectionInfo
from .protocol import RemoteMessageType, SERVER_PORT

try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning(
		"Unable to initialise translations. This may be because the addon is running from NVDA scratchpad."
	)

WX_VERSION = int(wx.version()[0])
WX_CENTER = wx.Center if WX_VERSION>=4 else wx.CENTER_ON_SCREEN

class ClientPanel(wx.Panel):
	host: wx.ComboBox
	key: wx.TextCtrl
	generate_key: wx.Button
	keyConnector: Optional['transport.RelayTransport']

	def __init__(self, parent: Optional[wx.Window] = None, id: int = wx.ID_ANY):
		super().__init__(parent, id)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of an edit field in connect dialog to enter name or address of the remote computer.
		sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&Host:")))
		self.host = wx.ComboBox(self, wx.ID_ANY)
		sizer.Add(self.host)
		# Translators: Label of the edit field to enter key (password) to secure the remote connection.
		sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&Key:")))
		self.key = wx.TextCtrl(self, wx.ID_ANY)
		sizer.Add(self.key)
		# Translators: The button used to generate a random key/password.
		self.generate_key = wx.Button(parent=self, label=_("&Generate Key"))
		self.generate_key.Bind(wx.EVT_BUTTON, self.on_generate_key)
		sizer.Add(self.generate_key)
		self.SetSizerAndFit(sizer)

	def on_generate_key(self, evt: wx.CommandEvent) -> None:
		if not self.host.GetValue():
			gui.messageBox(_("Host must be set."), _("Error"), wx.OK | wx.ICON_ERROR)
			self.host.SetFocus()
		else:
			evt.Skip()
			self.generate_key_command()

	def generate_key_command(self, insecure: bool = False) -> None:
			address = socket_utils.addressToHostPort(self.host.GetValue())
			self.keyConnector = transport.RelayTransport(address=address, serializer=serializer.JSONSerializer(), insecure=insecure)
			self.keyConnector.registerInbound(RemoteMessageType.generate_key, self.handle_key_generated)
			self.keyConnector.transportCertificateAuthenticationFailed.register(self.handle_certificate_failed)
			t = threading.Thread(target=self.keyConnector.run)
			t.start()

	@alwaysCallAfter
	def handle_key_generated(self, key: Optional[str] = None) -> None:
		self.key.SetValue(key)
		self.key.SetFocus()
		self.keyConnector.close()
		self.keyConnector = None

	@alwaysCallAfter
	def handle_certificate_failed(self) -> None:
		try:
			cert_hash = self.keyConnector.lastFailFingerprint
				
			wnd = CertificateUnauthorizedDialog(None, fingerprint=cert_hash)
			a = wnd.ShowModal()
			if a == wx.ID_YES:
				config = configuration.get_config()
				config['trusted_certs'][self.host.GetValue()]=cert_hash
				config.write()
			if a != wx.ID_YES and a != wx.ID_NO: return
		except Exception as ex:
			log.error(ex)
			return
		self.keyConnector.close()
		self.keyConnector = None
		self.generate_key_command(True)

class ServerPanel(wx.Panel):
	get_IP: wx.Button
	external_IP: wx.TextCtrl
	port: wx.TextCtrl
	key: wx.TextCtrl
	generate_key: wx.Button

	def __init__(self, parent: Optional[wx.Window] = None, id: int = wx.ID_ANY):
		super().__init__(parent, id)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Used in server mode to obtain the external IP address for the server (controlled computer) for direct connection.
		self.get_IP = wx.Button(parent=self, label=_("Get External &IP"))
		self.get_IP.Bind(wx.EVT_BUTTON, self.on_get_IP)
		sizer.Add(self.get_IP)
		# Translators: Label of the field displaying the external IP address if using direct (client to server) connection.
		sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&External IP:")))
		self.external_IP = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_READONLY|wx.TE_MULTILINE)
		sizer.Add(self.external_IP)
		# Translators: The label of an edit field in connect dialog to enter the port the server will listen on.
		sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&Port:")))
		self.port = wx.TextCtrl(self, wx.ID_ANY, value=str(SERVER_PORT))
		sizer.Add(self.port)
		sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&Key:")))
		self.key = wx.TextCtrl(self, wx.ID_ANY)
		sizer.Add(self.key)
		self.generate_key = wx.Button(parent=self, label=_("&Generate Key"))
		self.generate_key.Bind(wx.EVT_BUTTON, self.on_generate_key)
		sizer.Add(self.generate_key)
		self.SetSizerAndFit(sizer)

	def on_generate_key(self, evt: wx.CommandEvent) -> None:
		evt.Skip()
		res = str(random.randrange(1, 9))
		for n in range(6):
			res += str(random.randrange(0, 9))
		self.key.SetValue(res)
		self.key.SetFocus()

	def on_get_IP(self, evt: wx.CommandEvent) -> None:
		evt.Skip()
		self.get_IP.Enable(False)
		t = threading.Thread(target=self.do_portcheck, args=[int(self.port.GetValue())])
		t.daemon = True
		t.start()

	def do_portcheck(self, port: int) -> None:
		temp_server = server.LocalRelayServer(port=port, password=None)
		try:
			req = request.urlopen('https://portcheck.nvdaremote.com/port/%s' % port)
			data = req.read()
			result = json.loads(data)
			wx.CallAfter(self.on_get_IP_success, result)
		except Exception as e:
			wx.CallAfter(self.on_get_IP_fail, e)
			raise
		finally:
			temp_server.close()
			wx.CallAfter(self.get_IP.Enable, True)

	def on_get_IP_success(self, data: Dict[str, Any]) -> None:
		ip = data['host']
		port = data['port']
		is_open = data['open']
		if is_open:
			wx.MessageBox(message=_("Successfully retrieved IP address. Port {port} is open.").format(port=port), caption=_("Success"), style=wx.OK)
		else:
			wx.MessageBox(message=_("Retrieved external IP, but port {port} is not currently forwarded.".format(port=port)), caption=_("Warning"), style=wx.ICON_WARNING|wx.OK)
		self.external_IP.SetValue(ip)
		self.external_IP.SetSelection(0, len(ip))
		self.external_IP.SetFocus()

	def on_get_IP_fail(self, exc: Exception) -> None:
		wx.MessageBox(message=_("Unable to contact portcheck server, please manually retrieve your IP address"), caption=_("Error"), style=wx.ICON_ERROR|wx.OK)

class DirectConnectDialog(wx.Dialog):
	client_or_server: wx.RadioBox
	connection_type: wx.RadioBox
	container: wx.Panel
	panel: Union[ClientPanel, ServerPanel]
	main_sizer: wx.BoxSizer

	def __init__(self, parent: wx.Window, id: int, title: str):
		super().__init__(parent, id, title=title)
		main_sizer = self.main_sizer = wx.BoxSizer(wx.VERTICAL)
		self.client_or_server = wx.RadioBox(self, wx.ID_ANY, choices=(_("Client"), _("Server")), style=wx.RA_VERTICAL)
		self.client_or_server.Bind(wx.EVT_RADIOBOX, self.onClientOrServer)
		self.client_or_server.SetSelection(0)
		main_sizer.Add(self.client_or_server)
		choices = [_("Control another machine"), _("Allow this machine to be controlled")]
		self.connection_type = wx.RadioBox(self, wx.ID_ANY, choices=choices, style=wx.RA_VERTICAL)
		self.connection_type.SetSelection(0)
		main_sizer.Add(self.connection_type)
		self.container = wx.Panel(parent=self)
		self.panel = ClientPanel(parent=self.container)
		main_sizer.Add(self.container)
		buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		main_sizer.Add(buttons, flag=wx.BOTTOM)
		main_sizer.Fit(self)
		self.SetSizer(main_sizer)
		self.Center(wx.BOTH | WX_CENTER)
		ok = wx.FindWindowById(wx.ID_OK, self)
		ok.Bind(wx.EVT_BUTTON, self.onOk)
		self.client_or_server.SetFocus()

	def onClientOrServer(self, evt: wx.CommandEvent) -> None:
		evt.Skip()
		self.panel.Destroy()
		if self.client_or_server.GetSelection() == 0:
			self.panel = ClientPanel(parent=self.container)
		else:
			self.panel = ServerPanel(parent=self.container)
		self.main_sizer.Fit(self)

	def onOk(self, evt: wx.CommandEvent) -> None:
		if self.client_or_server.GetSelection() == 0 and (not self.panel.host.GetValue() or not self.panel.key.GetValue()):
			gui.messageBox(_("Both host and key must be set."), _("Error"), wx.OK | wx.ICON_ERROR)
			self.panel.host.SetFocus()
		elif self.client_or_server.GetSelection() == 1 and not self.panel.port.GetValue() or not self.panel.key.GetValue():
			gui.messageBox(_("Both port and key must be set."), _("Error"), wx.OK | wx.ICON_ERROR)
			self.panel.port.SetFocus()
		else:
			evt.Skip()

	def getKey(self) -> str:
		return self.panel.key.GetValue()
	
	def getConnectionInfo(self) -> ConnectionInfo:
		if self.client_or_server.GetSelection() == 0:  # client
			host = self.panel.host.GetValue()
			serverAddr, port = socket_utils.addressToHostPort(host)
			mode = 'master' if self.connection_type.GetSelection() == 0 else 'slave'
			return ConnectionInfo(
				hostname=serverAddr, 
				mode=mode, 
				key=self.getKey(), 
				port=port
			)
		else:  # server
			port = int(self.panel.port.GetValue())
			mode = 'master' if self.connection_type.GetSelection() == 0 else 'slave'
			return ConnectionInfo(
				hostname='127.0.0.1',
				mode=mode,
				key=self.getKey(),
				port=port
			)
	
class CertificateUnauthorizedDialog(wx.MessageDialog):
	def __init__(self, parent: Optional[wx.Window], fingerprint: Optional[str] = None):
		# Translators: A title bar of a window presented when an attempt has been made to connect with a server with unauthorized certificate.
		title=_("NVDA Remote Connection Security Warning")
		# Translators: A message of a window presented when an attempt has been made to connect with a server with unauthorized certificate.
		message = _("Warning! The certificate of this server could not be verified.\nThis connection may not be secure. It is possible that someone is trying to overhear your communication.\nBefore continuing please make sure that the following server certificate fingerprint is a proper one.\nIf you have any questions, please contact the server administrator.\n\nServer SHA256 fingerprint: {fingerprint}\n\nDo you want to continue connecting?").format(fingerprint=fingerprint)
		super().__init__(parent, caption=title, message=message, style=wx.YES_NO|wx.CANCEL|wx.CANCEL_DEFAULT|wx.CENTRE)
		self.SetYesNoLabels(_("Connect and do not ask again for this server"), _("Connect"))
