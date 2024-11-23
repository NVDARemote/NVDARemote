import wx
import gui
from gui.settingsDialogs import SettingsPanel
from . import configuration

class RemoteSettingsPanel(SettingsPanel):
	# Translators: This is the label for the remote settings category in NVDA Settings screen.
	title = _("Remote")
	autoconnect: wx.CheckBox
	client_or_server: wx.RadioBox
	connection_type: wx.RadioBox
	host: wx.TextCtrl
	port: wx.SpinCtrl
	key: wx.TextCtrl
	play_sounds: wx.CheckBox
	delete_fingerprints: wx.Button

	def makeSettings(self, settingsSizer):
		self.config = configuration.get_config()
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.autoconnect = wx.CheckBox(self, wx.ID_ANY, label=_("Auto-connect to control server on startup"))
		self.autoconnect.Bind(wx.EVT_CHECKBOX, self.on_autoconnect)
		sHelper.addItem(self.autoconnect)
		#Translators: Whether or not to use a relay server when autoconnecting
		self.client_or_server = wx.RadioBox(self, wx.ID_ANY, choices=(_("Use Remote Control Server"), _("Host Control Server")), style=wx.RA_VERTICAL)
		self.client_or_server.Bind(wx.EVT_RADIOBOX, self.on_client_or_server)
		self.client_or_server.SetSelection(0)
		self.client_or_server.Enable(False)
		sHelper.addItem(self.client_or_server)
		choices = [_("Allow this machine to be controlled"), _("Control another machine")]
		self.connection_type = wx.RadioBox(self, wx.ID_ANY, choices=choices, style=wx.RA_VERTICAL)
		self.connection_type.SetSelection(0)
		self.connection_type.Enable(False)
		sHelper.addItem(self.connection_type)
		sHelper.addItem(wx.StaticText(self, wx.ID_ANY, label=_("&Host:")))
		self.host = wx.TextCtrl(self, wx.ID_ANY)
		self.host.Enable(False)
		sHelper.addItem(self.host)
		sHelper.addItem(wx.StaticText(self, wx.ID_ANY, label=_("&Port:")))
		self.port = wx.SpinCtrl(self, wx.ID_ANY, min=1, max=65535)
		self.port.Enable(False)
		sHelper.addItem(self.port)
		sHelper.addItem(wx.StaticText(self, wx.ID_ANY, label=_("&Key:")))
		self.key = wx.TextCtrl(self, wx.ID_ANY)
		self.key.Enable(False)
		sHelper.addItem(self.key)
		# Translators: A checkbox in add-on options dialog to set whether sounds play instead of beeps.
		self.play_sounds = wx.CheckBox(self, wx.ID_ANY, label=_("Play sounds instead of beeps"))
		sHelper.addItem(self.play_sounds)
		# Translators: A button in add-on options dialog to delete all fingerprints of unauthorized certificates.
		self.delete_fingerprints = wx.Button(self, wx.ID_ANY, label=_("Delete all trusted fingerprints"))
		self.delete_fingerprints.Bind(wx.EVT_BUTTON, self.on_delete_fingerprints)
		sHelper.addItem(self.delete_fingerprints)
		self.set_from_config()

	def on_autoconnect(self, evt: wx.CommandEvent) -> None:
		self.set_controls()

	def set_controls(self) -> None:
		state = bool(self.autoconnect.GetValue())
		self.client_or_server.Enable(state)
		self.connection_type.Enable(state)
		self.key.Enable(state)
		self.host.Enable(not bool(self.client_or_server.GetSelection()) and state)
		self.port.Enable(bool(self.client_or_server.GetSelection()) and state)

	def on_client_or_server(self, evt: wx.CommandEvent) -> None:
		evt.Skip()
		self.set_controls()

	def set_from_config(self) -> None:
		cs = self.config['controlserver']
		self_hosted = cs['self_hosted']
		connection_type = cs['connection_type']
		self.autoconnect.SetValue(cs['autoconnect'])
		self.client_or_server.SetSelection(int(self_hosted))
		self.connection_type.SetSelection(connection_type)
		self.host.SetValue(cs['host'])
		self.port.SetValue(str(cs['port']))
		self.key.SetValue(cs['key'])
		self.set_controls()
		self.play_sounds.SetValue(self.config['ui']['play_sounds'])

	def on_delete_fingerprints(self, evt: wx.CommandEvent) -> None:
		if gui.messageBox(_("When connecting to an unauthorized server, you will again be prompted to accepts its certificate."), _("Are you sure you want to delete all stored trusted fingerprints?"), wx.YES|wx.NO|wx.NO_DEFAULT|wx.ICON_WARNING) == wx.YES:
			self.config['trusted_certs'].clear()
			self.config.write()
		evt.Skip()

	def isValid(self) -> bool:
		if self.autoconnect.GetValue():
			if not self.client_or_server.GetSelection() and (not self.host.GetValue() or not self.key.GetValue()):
				gui.messageBox(_("Both host and key must be set in the Remote section."), _("Remote Error"), wx.OK | wx.ICON_ERROR)
				return False
			elif self.client_or_server.GetSelection() and not self.port.GetValue() or not self.key.GetValue():
				gui.messageBox(_("Both port and key must be set in the Remote section."), _("Remote Error"), wx.OK | wx.ICON_ERROR)
				return False
		return True

	def write_to_config(self) -> None:
		cs = self.config['controlserver']
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
		self.config['ui']['play_sounds'] = self.play_sounds.GetValue()
		self.config.write()

	def onSave(self):
		self.write_to_config()