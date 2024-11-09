import hashlib
from collections import defaultdict

import addonHandler
import braille
import gui
import speech
import ui
import versionInfo
from logHandler import log

from . import configuration, connection_info, cues, nvda_patcher
from .transport import TransportEvents, RelayTransport

addonHandler.initTranslation()
if not (
	versionInfo.version_year >= 2021 or
	(versionInfo.version_year == 2020 and versionInfo.version_major >= 2)
):
	# NVDA versions newer than 2020.2 have a _CancellableSpeechCommand which should be ignored by NVDA remote
	# For older versions, we create a dummy command that won't cause existing commands to be ignored.
	class _DummyCommand(speech.commands.SpeechCommand): pass
	speech.commands._CancellableSpeechCommand = _DummyCommand


EXCLUDED_SPEECH_COMMANDS = (
	speech.commands.BaseCallbackCommand,
	# _CancellableSpeechCommands are not designed to be reported and are used internally by NVDA. (#230)
	speech.commands._CancellableSpeechCommand,
)

class RemoteSession:
	"""Base class for a session that runs on either the master or slave machine."""

	transport: RelayTransport

	def __init__(self, local_machine, transport: RelayTransport):
		self.local_machine = local_machine
		self.patcher = None
		self.transport = transport
		self.transport.callback_manager.registerCallback('msg_version_mismatch', self.handle_version_mismatch)
		self.transport.callback_manager.registerCallback('msg_motd', self.handle_motd)

	def handle_version_mismatch(self, **kwargs):
		#translators: Message for version mismatch
		message = _("""The version of the relay server which you have connected to is not compatible with this version of the Remote Client.
Please either use a different server or upgrade your version of the addon.""")
		ui.message(message)
		self.transport.close()

	def handle_motd(self, motd: str, force_display=False, **kwargs):
		if force_display or self.shouldDisplayMotd(motd):
			gui.messageBox(parent=gui.mainFrame, caption=_("Message of the Day"), message=motd)

	def shouldDisplayMotd(self, motd: str):
		conf = configuration.get_config()
		host, port = self.transport.address
		host = host.lower()
		address = '{host}:{port}'.format(host=host, port=port)
		motdBytes = motd.encode('utf-8', errors='surrogatepass')
		hashed = hashlib.sha1(motdBytes).hexdigest()
		current = conf['seen_motds'].get(address, "")
		if current == hashed:
			return False
		conf['seen_motds'][address] = hashed
		conf.write()
		return True

class SlaveSession(RemoteSession):
	"""Session that runs on the slave and manages state."""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.transport.callback_manager.registerCallback('msg_client_joined', self.handle_client_connected)
		self.transport.callback_manager.registerCallback('msg_client_left', self.handle_client_disconnected)
		self.transport.callback_manager.registerCallback('msg_key', self.local_machine.send_key)
		self.masters = defaultdict(dict)
		self.master_display_sizes = []

		self.transport.callback_manager.registerCallback('msg_index', self.recv_index)
		self.transport.callback_manager.registerCallback(TransportEvents.CLOSING, self.handle_transport_closing)
		self.patcher = nvda_patcher.NVDASlavePatcher()
		self.patch_callbacks_added = False
		self.transport.callback_manager.registerCallback('msg_channel_joined', self.handle_channel_joined)
		self.transport.callback_manager.registerCallback('msg_set_clipboard_text', self.local_machine.set_clipboard_text)
		self.transport.callback_manager.registerCallback('msg_set_braille_info', self.handleBrailleInfo)
		self.transport.callback_manager.registerCallback('msg_set_display_size', self.setDisplaySize)
		if versionInfo.version_year >= 2023:
			braille.filter_displaySize.register(self.local_machine.handle_filter_displaySize)
		self.transport.callback_manager.registerCallback('msg_braille_input', self.local_machine.braille_input)
		self.transport.callback_manager.registerCallback('msg_send_SAS', self.local_machine.send_SAS)


	def get_connection_info(self):
		hostname, port = self.transport.address
		key = self.transport.channel
		return connection_info.ConnectionInfo(hostname=hostname, port=port, key=key, mode='slave')

	def handle_client_connected(self, client=None, **kwargs):
		self.patcher.patch()
		if not self.patch_callbacks_added:
			self.addPatchCallbacks()
			self.patch_callbacks_added = True
		cues.client_connected()
		if client['connection_type'] == 'master':
			self.masters[client['id']]['active'] = True

	def handle_channel_joined(self, channel=None, clients=None, origin=None, **kwargs):
		if clients is None:
			clients = []
		for client in clients:
			self.handle_client_connected(client)

	def handle_transport_closing(self):
		self.patcher.unpatch()
		if self.patch_callbacks_added:
			self.removePatchCallbacks()
			self.patch_callbacks_added = False

	def handle_transport_disconnected(self):
		cues.client_connected()
		self.patcher.unpatch()

	def handle_client_disconnected(self, client=None, **kwargs):
		cues.client_disconnected()
		if client['connection_type'] == 'master':
			del self.masters[client['id']]
		if not self.masters:
			self.patcher.unpatch()

	def setDisplaySize(self, sizes=None, **kwargs):
		self.master_display_sizes = sizes if sizes else [info.get("braille_numCells", 0) for info in self.masters.values()]
		self.local_machine.set_braille_display_size(self.master_display_sizes)

	def handleBrailleInfo(self, name=None, numCells=0, origin=None, **kwargs):
		if not self.masters.get(origin):
			return
		self.masters[origin]['braille_name'] = name
		self.masters[origin]['braille_numCells'] = numCells
		self.setDisplaySize()

	def _getPatcherCallbacks(self):
		return (
			('speak', self.speak),
			('beep', self.beep),
			('wave', self.playWaveFile),
			('cancel_speech', self.cancel_speech),
			('pause_speech', self.pause_speech),
			('display', self.display),
			('set_display', self.setDisplaySize)
		)

	def addPatchCallbacks(self):
		patcher_callbacks = self._getPatcherCallbacks()
		for event, callback in patcher_callbacks:
			self.patcher.registerCallback(event, callback)

	def removePatchCallbacks(self):
		patcher_callbacks = self._getPatcherCallbacks()
		for event, callback in patcher_callbacks:
			self.patcher.unregisterCallback(event, callback)

	def _filterUnsupportedSpeechCommands(self, speechSequence):
		return list([
			item for item in speechSequence
			if not isinstance(item, EXCLUDED_SPEECH_COMMANDS)
		])

	def speak(self, speechSequence, priority):
		self.transport.send(
			type="speak",
			sequence=self._filterUnsupportedSpeechCommands(speechSequence),
			priority=priority
		)

	def cancel_speech(self):
		self.transport.send(type="cancel")

	def pause_speech(self, switch):
		self.transport.send(type="pause_speech", switch=switch)

	def beep(self, hz, length, left=50, right=50, **kwargs):
		self.transport.send(type='tone', hz=hz, length=length, left=left, right=right, **kwargs)

	def playWaveFile(self, **kwargs):
		"""This machine played a sound, send it to Master machine"""
		kwargs.update({
			# nvWave.playWaveFile should always be asynchronous when called from NVDA remote, so always send 'True'
			# Version 2.2 requires 'async' keyword.
			'async': True,
			# Version 2.3 onwards. Not currently used, but matches arguments for nvWave.playWaveFile.
			# Including it allows for forward compatibility if requirements change.
			'asynchronous': True,
		})
		self.transport.send(type='wave', **kwargs)

	def display(self, cells):
		# Only send braille data when there are controlling machines with a braille display
		if self.has_braille_masters():
			self.transport.send(type="display", cells=cells)

	def has_braille_masters(self):
		return bool([i for i in self.master_display_sizes if i>0])

	def recv_index(self, index=None, **kwargs):
		pass  # speech index approach changed in 2019.3

class MasterSession(RemoteSession):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.slaves = defaultdict(dict)
		self.patcher = nvda_patcher.NVDAMasterPatcher()
		self.patch_callbacks_added = False
		self.transport.callback_manager.registerCallback('msg_speak', self.local_machine.speak)
		self.transport.callback_manager.registerCallback('msg_cancel', self.local_machine.cancel_speech)
		self.transport.callback_manager.registerCallback('msg_pause_speech', self.local_machine.pause_speech)
		self.transport.callback_manager.registerCallback('msg_tone', self.local_machine.beep)
		self.transport.callback_manager.registerCallback('msg_wave', self.handle_play_wave)
		self.transport.callback_manager.registerCallback('msg_display', self.local_machine.display)
		self.transport.callback_manager.registerCallback('msg_nvda_not_connected', self.handle_nvda_not_connected)
		self.transport.callback_manager.registerCallback('msg_client_joined', self.handle_client_connected)
		self.transport.callback_manager.registerCallback('msg_client_left', self.handle_client_disconnected)
		self.transport.callback_manager.registerCallback('msg_channel_joined', self.handle_channel_joined)
		self.transport.callback_manager.registerCallback('msg_set_clipboard_text', self.local_machine.set_clipboard_text)
		self.transport.callback_manager.registerCallback('msg_send_braille_info', self.send_braille_info)
		self.transport.callback_manager.registerCallback(TransportEvents.CONNECTED, self.handle_connected)
		self.transport.callback_manager.registerCallback(TransportEvents.DISCONNECTED, self.handle_disconnected)

	def handle_play_wave(self, **kwargs):
		"""Receive instruction to play a 'wave' from the slave machine
		This method handles translation (between versions of NVDA Remote) of arguments required for 'msg_wave'
		"""
		# Note:
		# Version 2.2 will send only 'async' in kwargs
		# Version 2.3 will send 'asynchronous' and 'async' in kwargs
		if "fileName" not in kwargs:
			log.error("'fileName' missing from kwargs.")
			return
		fileName = kwargs.pop("fileName")
		self.local_machine.play_wave(fileName=fileName)

	def get_connection_info(self):
		hostname, port = self.transport.address
		key = self.transport.channel
		return connection_info.ConnectionInfo(hostname=hostname, port=port, key=key, mode='master')

	def handle_nvda_not_connected(self):
		speech.cancelSpeech()
		ui.message(_("Remote NVDA not connected."))

	def handle_connected(self):
		# speech index approach changed in 2019.3
		pass  # nothing to do

	def handle_disconnected(self):
		# speech index approach changed in 2019.3
		pass  # nothing to do

	def handle_channel_joined(self, channel=None, clients=None, origin=None, **kwargs):
		if clients is None:
			clients = []
		for client in clients:
			self.handle_client_connected(client)

	def handle_client_connected(self, client=None, **kwargs):
		self.patcher.patch()
		if not self.patch_callbacks_added:
			self.addPatchCallbacks()
			self.patch_callbacks_added = True
		self.send_braille_info()
		cues.client_connected()

	def handle_client_disconnected(self, client=None, **kwargs):
		self.patcher.unpatch()
		if self.patch_callbacks_added:
			self.removePatchCallbacks()
			self.patch_callbacks_added = False
		cues.client_disconnected()

	def send_braille_info(self, display=None, displaySize=None, **kwargs):
		if display is None:
			display = braille.handler.display
		if displaySize is None:
			displaySize = braille.handler.displaySize
		self.transport.send(type="set_braille_info", name=display.name, numCells=displaySize)

	def braille_input(self,**kwargs):
		self.transport.send(type="braille_input", **kwargs)

	def addPatchCallbacks(self):
		patcher_callbacks = (('braille_input', self.braille_input), ('set_display', self.send_braille_info))
		for event, callback in patcher_callbacks:
			self.patcher.registerCallback(event, callback)

	def removePatchCallbacks(self):
		patcher_callbacks = (('braille_input', self.braille_input), ('set_display', self.send_braille_info))
		for event, callback in patcher_callbacks:
			self.patcher.unregisterCallback(event, callback)
