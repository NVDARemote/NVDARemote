from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import threading
import time
from . import connection_info
import gui
import speech
import ui
import tones
import braille
from . import configuration
from . import nvda_patcher
from collections import defaultdict
from . import connection_info
import hashlib

class RemoteSession(object):

	def __init__(self, local_machine, transport):
		self.local_machine = local_machine
		self.patcher = None
		self.transport = transport
		self.transport.callback_manager.register_callback('msg_version_mismatch', self.handle_version_mismatch)
		self.transport.callback_manager.register_callback('msg_motd', self.handle_motd)

	def handle_version_mismatch(self, **kwargs):
		#translators: Message for version mismatch
		message = _("""The version of the relay server which you have connected to is not compatible with this version of the Remote Client.
Please either use a different server or upgrade your version of the addon.""")
		ui.message(message)
		self.transport.close()

	def handle_motd(self, motd, force_display=False, **kwargs):
		if force_display or self.should_display_motd(motd):
			gui.messageBox(parent=gui.mainFrame, caption=_("Message of the Day"), message=motd)

	def should_display_motd(self, motd):
		conf = configuration.get_config()
		host, port = self.transport.address
		host = host.lower()
		address = '{host}:{port}'.format(host=host, port=port)
		hashed = hashlib.sha1(motd).hexdigest()
		current = conf['seen_motds'].get(address, "")
		if current == hashed:
			return False
		conf['seen_motds'][address] = hashed
		conf.write()
		return True

class SlaveSession(RemoteSession):	
	"""Session that runs on the slave and manages state."""

	def __init__(self, *args, **kwargs):
		super(SlaveSession, self).__init__(*args, **kwargs)
		self.transport.callback_manager.register_callback('msg_client_joined', self.handle_client_connected)
		self.transport.callback_manager.register_callback('msg_client_left', self.handle_client_disconnected)
		self.transport.callback_manager.register_callback('msg_key', self.local_machine.send_key)
		self.masters = defaultdict(dict)
		self.master_display_sizes=[]
		self.last_client_index = None
		self.transport.callback_manager.register_callback('msg_index', self.update_index)
		self.transport.callback_manager.register_callback('transport_closing', self.handle_transport_closing)
		self.patcher = nvda_patcher.NVDASlavePatcher()
		self.patch_callbacks_added = False
		self.transport.callback_manager.register_callback('msg_channel_joined', self.handle_channel_joined)
		self.transport.callback_manager.register_callback('msg_set_clipboard_text', self.local_machine.set_clipboard_text)
		self.transport.callback_manager.register_callback('msg_set_braille_info', self.handle_braille_info)
		self.transport.callback_manager.register_callback('msg_set_display_size', self.set_display_size)
		self.transport.callback_manager.register_callback('msg_braille_input', self.local_machine.braille_input)
		self.transport.callback_manager.register_callback('msg_send_SAS', self.local_machine.send_SAS)


	def get_connection_info(self):
		hostname, port = self.transport.address
		key = self.transport.channel
		return connection_info.ConnectionInfo(hostname=hostname, port=port, key=key, mode='slave')

	def handle_client_connected(self, client=None, **kwargs):
		self.patcher.patch()
		if not self.patch_callbacks_added:
			self.add_patch_callbacks()
			self.patch_callbacks_added = True
		self.patcher.orig_beep(1000, 300)
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
			self.remove_patch_callbacks()
			self.patch_callbacks_added = False

	def handle_transport_disconnected(self):
		self.patcher.orig_beep(1000, 300)
		self.patcher.unpatch()

	def handle_client_disconnected(self, client=None, **kwargs):
		self.patcher.orig_beep(108, 300)
		if client['connection_type'] == 'master':
			del self.masters[client['id']]
		if not self.masters:
			self.patcher.unpatch()

	def set_display_size(self, sizes=None, **kwargs):
		self.master_display_sizes = sizes if sizes else [info.get("braille_numCells", 0) for info in self.masters.values()]
		self.local_machine.set_braille_display_size(self.master_display_sizes)

	def handle_braille_info(self, name=None, numCells=0, origin=None, **kwargs):
		if not self.masters.get(origin):
			return
		self.masters[origin]['braille_name'] = name
		self.masters[origin]['braille_numCells'] = numCells
		self.set_display_size()

	def add_patch_callbacks(self):
		patcher_callbacks = (('speak', self.speak), ('beep', self.beep), ('wave', self.playWaveFile), ('cancel_speech', self.cancel_speech), ('display', self.display), ('set_display', self.set_display_size))
		for event, callback in patcher_callbacks:
			self.patcher.register_callback(event, callback)
		self.patcher.set_last_index_callback(self._get_lastIndex)

	def remove_patch_callbacks(self):
		patcher_callbacks = (('speak', self.speak), ('beep', self.beep), ('wave', self.playWaveFile), ('cancel_speech', self.cancel_speech), ('display', self.display), ('set_display', self.set_display_size))
		for event, callback in patcher_callbacks:
			self.patcher.unregister_callback(event, callback)

	def speak(self, speechSequence):
		self.transport.send(type="speak", sequence=speechSequence)

	def cancel_speech(self):
		self.transport.send(type="cancel")

	def _get_lastIndex(self):
		return self.last_client_index

	def beep(self, hz, length, left=50, right=50):
		self.transport.send(type='tone', hz=hz, length=length, left=left, right=right)

	def playWaveFile(self, fileName, asynchronous=True):
		self.transport.send(type='wave', fileName=fileName, asynchronous=asynchronous)

	def display(self, cells):
		# Only send braille data when there are controlling machines with a braille display
		if self.has_braille_masters():
			self.transport.send(type="display", cells=cells)

	def has_braille_masters(self):
		return bool([i for i in self.master_display_sizes if i>0])

	def update_index(self, index=None, **kwargs):
		self.last_client_index = index

class MasterSession(RemoteSession):

	def __init__(self, *args, **kwargs):
		super(MasterSession, self).__init__(*args, **kwargs)
		self.slaves = defaultdict(dict)
		self.index_thread = None
		self.patcher = nvda_patcher.NVDAMasterPatcher()
		self.patch_callbacks_added = False
		self.transport.callback_manager.register_callback('msg_speak', self.local_machine.speak)
		self.transport.callback_manager.register_callback('msg_cancel', self.local_machine.cancel_speech)
		self.transport.callback_manager.register_callback('msg_tone', self.local_machine.beep)
		self.transport.callback_manager.register_callback('msg_wave', self.local_machine.play_wave)
		self.transport.callback_manager.register_callback('msg_display', self.local_machine.display)
		self.transport.callback_manager.register_callback('msg_nvda_not_connected', self.handle_nvda_not_connected)
		self.transport.callback_manager.register_callback('msg_client_joined', self.handle_client_connected)
		self.transport.callback_manager.register_callback('msg_client_left', self.handle_client_disconnected)
		self.transport.callback_manager.register_callback('msg_channel_joined', self.handle_channel_joined)
		self.transport.callback_manager.register_callback('msg_set_clipboard_text', self.local_machine.set_clipboard_text)
		self.transport.callback_manager.register_callback('msg_send_braille_info', self.send_braille_info)
		self.transport.callback_manager.register_callback('transport_connected', self.handle_connected)
		self.transport.callback_manager.register_callback('transport_disconnected', self.handle_disconnected)


	def get_connection_info(self):
		hostname, port = self.transport.address
		key = self.transport.channel
		return connection_info.ConnectionInfo(hostname=hostname, port=port, key=key, mode='master')

	def handle_nvda_not_connected(self):
		speech.cancelSpeech()
		ui.message(_("Remote NVDA not connected."))

	def handle_connected(self):
		if self.index_thread is not None:
			return
		self.index_thread = threading.Thread(target=self.send_indexes)
		self.index_thread.daemon = True
		self.index_thread.start()

	def handle_disconnected(self):
		self.index_thread = None

	def handle_channel_joined(self, channel=None, clients=None, origin=None, **kwargs):
		if clients is None:
			clients = []
		for client in clients:
			self.handle_client_connected(client)

	def handle_client_connected(self, client=None, **kwargs):
		self.patcher.patch()
		if not self.patch_callbacks_added:
			self.add_patch_callbacks()
			self.patch_callbacks_added = True
		self.send_braille_info()
		tones.beep(1000, 300)

	def handle_client_disconnected(self, client=None, **kwargs):
		self.patcher.unpatch()
		if self.patch_callbacks_added:
			self.remove_patch_callbacks()
			self.patch_callbacks_added = False
		tones.beep(108, 300)

	def send_braille_info(self):
		display=braille.handler.display
		self.transport.send(type="set_braille_info", name=display.name, numCells=display.numCells)

	def braille_input(self,**kwargs):
		self.transport.send(type="braille_input", **kwargs)

	def send_indexes(self):
		last = None
		POLL_TIME = 0.05
		while self.transport.connected:
			synth = speech.getSynth()
			if synth is None: #While switching synths
				time.sleep(POLL_TIME)
				continue
			index = synth.lastIndex
			if index != last:
				self.transport.send(type="index", index=index)
				last = index
			time.sleep(POLL_TIME)

	def add_patch_callbacks(self):
		patcher_callbacks = (('braille_input', self.braille_input), ('set_display', self.send_braille_info))
		for event, callback in patcher_callbacks:
			self.patcher.register_callback(event, callback)

	def remove_patch_callbacks(self):
		patcher_callbacks = (('braille_input', self.braille_input), ('set_display', self.send_braille_info))
		for event, callback in patcher_callbacks:
			self.patcher.unregister_callback(event, callback)
