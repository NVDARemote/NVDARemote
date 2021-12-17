import json
import random
import threading
from urllib import request
import wx
import gui
from . import serializer
from . import server
from . import transport
from . import socket_utils
from logHandler import log
import addonHandler
try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning(
		"Unable to initialise translations. This may be because the addon is running from NVDA scratchpad."
	)
from . import configuration

WX_VERSION = int(wx.version()[0])
WX_CENTER = wx.Center if WX_VERSION>=4 else wx.CENTER_ON_SCREEN

class ClientPanel(wx.Panel):

	def __init__(self, parent=None, id=wx.ID_ANY):
		super().__init__(parent, id)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of an edit field in connect dialog to enter name or address of the remote computer.
		sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&Host:")))
		self.host = wx.TextCtrl(self, wx.ID_ANY)
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

	def on_generate_key(self, evt):
		if not self.host.GetValue():
			gui.messageBox(_("Host must be set."), _("Error"), wx.OK | wx.ICON_ERROR)
			self.host.SetFocus()
		else:
			evt.Skip()
			self.generate_key_command()

	def generate_key_command(self, insecure=False):
			address = socket_utils.address_to_hostport(self.host.GetValue())
			self.key_connector = transport.RelayTransport(address=address, serializer=serializer.JSONSerializer(), insecure=insecure)
			self.key_connector.callback_manager.register_callback('msg_generate_key', self.handle_key_generated)
			self.key_connector.callback_manager.register_callback(transport.TransportEvents.CERTIFICATE_AUTHENTICATION_FAILED, self.handle_certificate_failed)
			t = threading.Thread(target=self.key_connector.run)
			t.start()

	def handle_key_generated(self, key=None):
		self.key.SetValue(key)
		self.key.SetFocus()
		self.key_connector.close()
		self.key_connector = None

	def handle_certificate_failed(self):
		try:
			cert_hash = self.key_connector.last_fail_fingerprint
				
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
		self.key_connector.close()
		self.key_connector = None
		self.generate_key_command(True)

class ServerPanel(wx.Panel):

	def __init__(self, parent=None, id=wx.ID_ANY):
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
		self.port = wx.TextCtrl(self, wx.ID_ANY, value=str(socket_utils.SERVER_PORT))
		sizer.Add(self.port)
		sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&Key:")))
		self.key = wx.TextCtrl(self, wx.ID_ANY)
		sizer.Add(self.key)
		self.generate_key = wx.Button(parent=self, label=_("&Generate Key"))
		self.generate_key.Bind(wx.EVT_BUTTON, self.on_generate_key)
		sizer.Add(self.generate_key)
		self.SetSizerAndFit(sizer)

	def on_generate_key(self, evt):
		evt.Skip()
		res = str(random.randrange(1, 9))
		for n in range(6):
			res += str(random.randrange(0, 9))
		self.key.SetValue(res)
		self.key.SetFocus()

	def on_get_IP(self, evt):
		evt.Skip()
		self.get_IP.Enable(False)
		t = threading.Thread(target=self.do_portcheck, args=[int(self.port.GetValue())])
		t.daemon = True
		t.start()

	def do_portcheck(self, port):
		temp_server = server.Server(port=port, password=None)
		try:
			req = request.urlopen('https://portcheck.nvdaremote.com/port/%s' % port)
			data = req.read()
			result = json.loads(data)
			wx.CallAfter(self.on_get_IP_success, result)
		except Exception as e:
			self.on_get_IP_fail(e)
			raise
		finally:
			temp_server.close()
			self.get_IP.Enable(True)

	def on_get_IP_success(self, data):
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


	def on_get_IP_fail(self, exc):
		wx.MessageBox(message=_("Unable to contact portcheck server, please manually retrieve your IP address"), caption=_("Error"), style=wx.ICON_ERROR|wx.OK)

class DirectConnectDialog(wx.Dialog):

	def __init__(self, parent, id, title):
		super().__init__(parent, id, title=title)
		main_sizer = self.main_sizer = wx.BoxSizer(wx.VERTICAL)
		self.client_or_server = wx.RadioBox(self, wx.ID_ANY, choices=(_("Client"), _("Server")), style=wx.RA_VERTICAL)
		self.client_or_server.Bind(wx.EVT_RADIOBOX, self.on_client_or_server)
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
		ok.Bind(wx.EVT_BUTTON, self.on_ok)
		self.client_or_server.SetFocus()

	def on_client_or_server(self, evt):
		evt.Skip()
		self.panel.Destroy()
		if self.client_or_server.GetSelection() == 0:
			self.panel = ClientPanel(parent=self.container)
		else:
			self.panel = ServerPanel(parent=self.container)
		self.main_sizer.Fit(self)

	def on_ok(self, evt):
		if self.client_or_server.GetSelection() == 0 and (not self.panel.host.GetValue() or not self.panel.key.GetValue()):
			gui.messageBox(_("Both host and key must be set."), _("Error"), wx.OK | wx.ICON_ERROR)
			self.panel.host.SetFocus()
		elif self.client_or_server.GetSelection() == 1 and not self.panel.port.GetValue() or not self.panel.key.GetValue():
			gui.messageBox(_("Both port and key must be set."), _("Error"), wx.OK | wx.ICON_ERROR)
			self.panel.port.SetFocus()
		else:
			evt.Skip()

class OptionsDialog(wx.Dialog):

	def __init__(self, parent, id, title):
		super().__init__(parent, id, title=title)
		main_sizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: A checkbox in add-on options dialog to set whether remote server is started when NVDA starts.
		self.autoconnect = wx.CheckBox(self, wx.ID_ANY, label=_("Auto-connect to control server on startup"))
		self.autoconnect.Bind(wx.EVT_CHECKBOX, self.on_autoconnect)
		main_sizer.Add(self.autoconnect)
		#Translators: Whether or not to use a relay server when autoconnecting
		self.client_or_server = wx.RadioBox(self, wx.ID_ANY, choices=(_("Use Remote Control Server"), _("Host Control Server")), style=wx.RA_VERTICAL)
		self.client_or_server.Bind(wx.EVT_RADIOBOX, self.on_client_or_server)
		self.client_or_server.SetSelection(0)
		self.client_or_server.Enable(False)
		main_sizer.Add(self.client_or_server)
		choices = [_("Allow this machine to be controlled"), _("Control another machine")]
		self.connection_type = wx.RadioBox(self, wx.ID_ANY, choices=choices, style=wx.RA_VERTICAL)
		self.connection_type.SetSelection(0)
		self.connection_type.Enable(False)
		main_sizer.Add(self.connection_type)
		main_sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&Host:")))
		self.host = wx.TextCtrl(self, wx.ID_ANY)
		self.host.Enable(False)
		main_sizer.Add(self.host)
		main_sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&Port:")))
		self.port = wx.TextCtrl(self, wx.ID_ANY)
		self.port.Enable(False)
		main_sizer.Add(self.port)
		main_sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&Key:")))
		self.key = wx.TextCtrl(self, wx.ID_ANY)
		self.key.Enable(False)
		main_sizer.Add(self.key)
		# Translators: A checkbox in add-on options dialog to set whether sounds play instead of beeps.
		self.play_sounds = wx.CheckBox(self, wx.ID_ANY, label=_("Play sounds instead of beeps"))
		main_sizer.Add(self.play_sounds)
		# Translators: A button in add-on options dialog to delete all fingerprints of unauthorized certificates.
		self.delete_fingerprints = wx.Button(self, wx.ID_ANY, label=_("Delete all trusted fingerprints"))
		self.delete_fingerprints.Bind(wx.EVT_BUTTON, self.on_delete_fingerprints)
		main_sizer.Add(self.delete_fingerprints)
		buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		main_sizer.Add(buttons, flag=wx.BOTTOM)
		main_sizer.Fit(self)
		self.SetSizer(main_sizer)
		self.Center(wx.BOTH | WX_CENTER)
		ok = wx.FindWindowById(wx.ID_OK, self)
		ok.Bind(wx.EVT_BUTTON, self.on_ok)
		self.autoconnect.SetFocus()

	def on_autoconnect(self, evt):
		self.set_controls()

	def set_controls(self):
		state = bool(self.autoconnect.GetValue())
		self.client_or_server.Enable(state)
		self.connection_type.Enable(state)
		self.key.Enable(state)
		self.host.Enable(not bool(self.client_or_server.GetSelection()) and state)
		self.port.Enable(bool(self.client_or_server.GetSelection()) and state)

	def on_client_or_server(self, evt):
		evt.Skip()
		self.set_controls()

	def set_from_config(self, config):
		cs = config['controlserver']
		self_hosted = cs['self_hosted']
		connection_type = cs['connection_type']
		self.autoconnect.SetValue(cs['autoconnect'])
		self.client_or_server.SetSelection(int(self_hosted))
		self.connection_type.SetSelection(connection_type)
		self.host.SetValue(cs['host'])
		self.port.SetValue(str(cs['port']))
		self.key.SetValue(cs['key'])
		self.set_controls()
		self.play_sounds.SetValue(config['ui']['play_sounds'])

	def on_delete_fingerprints(self, evt):
		if gui.messageBox(_("When connecting to an unauthorized server, you will again be prompted to accepts its certificate."), _("Are you sure you want to delete all stored trusted fingerprints?"), wx.YES|wx.NO|wx.NO_DEFAULT|wx.ICON_WARNING) == wx.YES:
			config = configuration.get_config()
			config['trusted_certs'].clear()
			config.write()
		evt.Skip()

	def on_ok(self, evt):
		if self.autoconnect.GetValue():
			if not self.client_or_server.GetSelection() and (not self.host.GetValue() or not self.key.GetValue()):
				gui.messageBox(_("Both host and key must be set."), _("Error"), wx.OK | wx.ICON_ERROR)
			elif self.client_or_server.GetSelection() and not self.port.GetValue() or not self.key.GetValue():
				gui.messageBox(_("Both port and key must be set."), _("Error"), wx.OK | wx.ICON_ERROR)
			else:
				evt.Skip()
		else:
			evt.Skip()

	def write_to_config(self, config):
		cs = config['controlserver']
		cs['autoconnect'] = self.autoconnect.GetValue()
		self_hosted = bool(self.client_or_server.GetSelection())
		connection_type = self.connection_type.GetSelection()
		cs['self_hosted'] = self_hosted
		cs['connection_type'] = connection_type
		if not self_hosted:
			cs['host'] = self.host.GetValue()
		else:
			cs['port'] = int(self.port.GetValue())
		cs['key'] = self.key.GetValue()
		config['ui']['play_sounds'] = self.play_sounds.GetValue()
		config.write()

class CertificateUnauthorizedDialog(wx.MessageDialog):

	def __init__(self, parent, fingerprint=None):
		# Translators: A title bar of a window presented when an attempt has been made to connect with a server with unauthorized certificate.
		title=_("NVDA Remote Connection Security Warning")
		# Translators: A message of a window presented when an attempt has been made to connect with a server with unauthorized certificate.
		message = _("Warning! The certificate of this server could not be verified.\nThis connection may not be secure. It is possible that someone is trying to overhear your communication.\nBefore continuing please make sure that the following server certificate fingerprint is a proper one.\nIf you have any questions, please contact the server administrator.\n\nServer SHA256 fingerprint: {fingerprint}\n\nDo you want to continue connecting?").format(fingerprint=fingerprint)
		super().__init__(parent, caption=title, message=message, style=wx.YES_NO|wx.CANCEL|wx.CANCEL_DEFAULT|wx.CENTRE)
		self.SetYesNoLabels(_("Connect and do not ask again for this server"), _("Connect"))
