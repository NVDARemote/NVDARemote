import json
import random
import threading
import urllib
import wx
import gui
import serializer
import server
import transport
import socket_utils

class ClientPanel(wx.Panel):

	def __init__(self, parent=None, id=wx.ID_ANY):
		super(ClientPanel, self).__init__(parent, id)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&Host:")))
		self.host = wx.TextCtrl(self, wx.ID_ANY, value="remote.accessolutions.fr")
		sizer.Add(self.host)
		sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&Key:")))
		self.key = wx.TextCtrl(self, wx.ID_ANY)
		sizer.Add(self.key)
		self.generate_key = wx.Button(parent=self, label=_("&Generate Key"))
		self.generate_key.Bind(wx.EVT_BUTTON, self.on_generate_key)
		sizer.Add(self.generate_key)
		self.SetSizerAndFit(sizer)

	def on_generate_key(self, evt):
		evt.Skip()
		address = socket_utils.address_to_hostport(self.host.GetValue())
		self.key_connector = transport.RelayTransport(address=address, serializer=serializer.JSONSerializer())
		self.key_connector.callback_manager.register_callback('msg_generate_key', self.handle_key_generated)
		t = threading.Thread(target=self.key_connector.run)
		t.start()

	def handle_key_generated(self, key=None):
		self.key.SetValue(key)
		self.key.SetFocus()
		self.key_connector.close()
		self.key_connector = None

class ServerPanel(wx.Panel):

	def __init__(self, parent=None, id=wx.ID_ANY):
		super(ServerPanel, self).__init__(parent, id)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.get_IP = wx.Button(parent=self, label=_("Get External &IP"))
		self.get_IP.Bind(wx.EVT_BUTTON, self.on_get_IP)
		sizer.Add(self.get_IP)
		sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&External IP:")))
		self.external_IP = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_READONLY|wx.TE_MULTILINE)
		sizer.Add(self.external_IP)
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
		for n in xrange(6):
			res += str(random.randrange(0, 9))
		self.key.SetValue(res)
		self.key.SetFocus()

	def on_get_IP(self, evt):
		evt.Skip()
		self.get_IP.Enable(False)
		t = threading.Thread(target=self.do_portcheck, args=[6837])
		t.daemon = True
		t.start()

	def do_portcheck(self, port):
		temp_server = server.Server(port=port, password=None)
		try:
			req = urllib.urlopen('https://portcheck.net/port/%s' % port)
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
			wx.MessageBox(message=_("Successfully retrieved IP address. Your port is open."), caption=_("Success"), style=wx.OK)
		else:
			wx.MessageBox(message=_("Retrieved external IP, but your port is not currently forwarded."), caption=_("Warning"), style=wx.ICON_WARNING|wx.OK)
		self.external_IP.SetValue(ip)
		self.external_IP.SetSelection(0, len(ip))
		self.external_IP.SetFocus()


	def on_get_IP_fail(self, exc):
		wx.MessageBox(message=_("Unable to contact portcheck server, please manually retrieve your IP address"), caption=_("Error"), style=wx.ICON_ERROR|wx.OK)

class DirectConnectDialog(wx.Dialog):

	def __init__(self, parent, id, title):
		super(DirectConnectDialog, self).__init__(parent, id, title=title)
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
		ok = wx.FindWindowById(wx.ID_OK, self)
		ok.Bind(wx.EVT_BUTTON, self.on_ok)

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
		elif self.client_or_server.GetSelection() == 1 and not self.panel.key.GetValue():
			gui.messageBox(_("Key must be set."), _("Error"), wx.OK | wx.ICON_ERROR)
			self.panel.key.SetFocus()
		else:
			evt.Skip()

class OptionsDialog(wx.Dialog):

	def __init__(self, parent, id, title):
		super(OptionsDialog, self).__init__(parent, id, title=title)
		main_sizer = wx.BoxSizer(wx.VERTICAL)
		self.autoconnect = wx.CheckBox(self, wx.ID_ANY, label=_("Auto-connect to control server on startup"))
		self.autoconnect.Bind(wx.EVT_CHECKBOX, self.on_autoconnect)
		main_sizer.Add(self.autoconnect)
		main_sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&Host:")))
		self.host = wx.TextCtrl(self, wx.ID_ANY)
		self.host.Enable(False)
		main_sizer.Add(self.host)
		main_sizer.Add(wx.StaticText(self, wx.ID_ANY, label=_("&Key:")))
		self.key = wx.TextCtrl(self, wx.ID_ANY)
		self.key.Enable(False)
		main_sizer.Add(self.key)
		buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		main_sizer.Add(buttons, flag=wx.BOTTOM)
		main_sizer.Fit(self)
		self.SetSizer(main_sizer)
		ok = wx.FindWindowById(wx.ID_OK, self)
		ok.Bind(wx.EVT_BUTTON, self.on_ok)
		self.autoconnect.SetFocus()

	def on_autoconnect(self, evt):
		self.set_controls()

	def set_controls(self):
		state = self.autoconnect.GetValue()
		self.host.Enable(state)
		self.key.Enable(state)

	def set_from_config(self, config):
		cs = config['controlserver']
		self.autoconnect.SetValue(cs['autoconnect'])
		self.host.SetValue(cs['host'])
		self.key.SetValue(cs['key'])
		self.set_controls()

	def on_ok(self, evt):
		if self.autoconnect.GetValue() and (not self.host.GetValue() or not self.key.GetValue()):
			gui.messageBox(_("Both host and key must be set."), _("Error"), wx.OK | wx.ICON_ERROR)
		else:
			evt.Skip()

	def write_to_config(self, config):
		cs = config['controlserver']
		cs['autoconnect'] = self.autoconnect.GetValue()
		cs['host'] = self.host.GetValue()
		cs['key'] = self.key.GetValue()
		config.write()
