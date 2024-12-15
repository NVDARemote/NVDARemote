import logging
import sys

import addonHandler
import ui
from globalPluginHandler import GlobalPlugin as _GlobalPlugin
from logHandler import log
from scriptHandler import script

from .client import RemoteClient

try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning(
		"Unable to initialise translations. This may be because the addon is running from NVDA scratchpad."
	)


logging.getLogger("keyboard_hook").addHandler(logging.StreamHandler(sys.stdout))

class GlobalPlugin(_GlobalPlugin):
	scriptCategory: str = _("NVDA Remote")
	client: RemoteClient

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.client = RemoteClient()
		self.client.registerLocalScript(self.script_sendKeys)

	def terminate(self):
		self.client.terminate()

	@script(
		description=_("""Mute or unmute the speech coming from the remote computer""")
	)
	def script_toggle_remote_mute(self, gesture):
		self.client.toggleMute()

	@script(
		gesture="kb:control+shift+NVDA+c",
		description=_("Sends the contents of the clipboard to the remote machine"),
	)
	def script_push_clipboard(self, gesture):
		self.client.pushClipboard()

	@script(description=_("""Copies a link to the remote session to the clipboard"""))
	def script_copy_link(self, gesture):
		self.client.copyLink()
		ui.message(_("Copied link"))

	@script(
		gesture="kb:alt+NVDA+pageDown", description=_("""Disconnect a remote session""")
	)
	def script_disconnect(self, gesture):
		if not self.client.isConnected:
			ui.message(_("Not connected."))
			return
		self.client.disconnect()

	@script(
		gesture="kb:alt+NVDA+pageUp", description=_("""Connect to a remote computer""")
	)
	def script_connect(self, gesture):
		if self.client.isConnected() or self.client.connecting:
			return
		self.client.doConnect()

	@script(
		# Translators: Documentation string for the script that toggles the control between guest and host machine.
		description=_("Toggles the control between guest and host machine"),
		gesture="kb:f11",
	)
	def script_sendKeys(self, gesture):
		self.client.toggleRemoteKeyControl(gesture)
