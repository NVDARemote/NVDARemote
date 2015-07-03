import callback_manager
import synthDriverHandler
import tones
import nvwave
import gui
import speech

class NVDAPatcher(callback_manager.CallbackManager):
	"""Class to manage patching of synth, tones, and nvwave."""

	def __init__(self):
		super(NVDAPatcher, self).__init__()
		self.orig_speak = None
		self.orig_cancel = None
		self.orig_get_lastIndex  = None
		self.last_index_callback = None
		self.orig_setSynth  = None
		self.orig_beep = None
		self.orig_playWaveFile = None

	def patch_synth(self):
		if self.orig_speak is not None:
			return
		synth = speech.getSynth()
		self.orig_speak = synth.speak
		synth.speak = self.speak
		self.orig_cancel = synth.cancel
		synth.cancel = self.cancel
		if synth.__class__.name == 'silence':
			def setter(self, val):
				pass
			self.orig_get_lastIndex = synth.__class__.lastIndex
			synth.__class__.lastIndex = property(fget=self._get_lastIndex, fset=setter)
		else:
			self.orig_get_lastIndex = synth.__class__.lastIndex.fget
			synth.__class__.lastIndex.fget = self._get_lastIndex
		self.orig_setSynth = synthDriverHandler.setSynth
		synthDriverHandler.setSynth = self.setSynth
		speech.setSynth = self.setSynth
		gui.settingsDialogs.setSynth = self.setSynth

	def patch_tones(self):
		if self.orig_beep is not None:
			return
		self.orig_beep = tones.beep
		tones.beep = self.beep

	def patch_nvwave(self):
		if self.orig_playWaveFile is not None:
			return
		self.orig_playWaveFile = nvwave.playWaveFile
		nvwave.playWaveFile = self.playWaveFile

	def unpatch_synth(self):
		if self.orig_speak is None:
			return
		synth = speech.getSynth()
		synth.speak = self.orig_speak
		self.orig_speak = None
		synth.cancel = self.orig_cancel
		self.orig_cancel = None
		if synth.__class__.name == 'silence':
			synth.__class__.lastIndex = self.orig_get_lastIndex
		else:
			synth.__class__.lastIndex.fget = self.orig_get_lastIndex
			self.orig_get_lastIndex = None
		synthDriverHandler.setSynth = self.orig_setSynth
		speech.setSynth = self.orig_setSynth
		gui.settingsDialogs.setSynth = self.orig_setSynth
		self.orig_setSynth = None

	def unpatch_tones(self):
		if self.orig_beep is None:
			return
		tones.beep = self.orig_beep
		self.orig_beep = None

	def unpatch_nvwave(self):
		if self.orig_playWaveFile is None:
			return
		nvwave.playWaveFile = self.orig_playWaveFile
		self.orig_playWaveFile = None

	def patch(self):
		self.patch_synth()
		self.patch_tones()
		self.patch_nvwave()

	def unpatch(self):
		self.unpatch_synth()
		self.unpatch_tones()
		self.unpatch_nvwave()

	def speak(self, speechSequence):
		self.call_callbacks('speak', speechSequence=speechSequence)
		self.orig_speak(speechSequence)

	def cancel(self):
		self.call_callbacks('cancel_speech')
		self.orig_cancel()

	def beep(self, hz, length, left=50, right=50):
		self.call_callbacks('beep', hz=hz, length=length, left=left, right=right)
		return self.orig_beep(hz=hz, length=length, left=left, right=right)

	def setSynth(self, *args, **kwargs):
		orig = self.orig_setSynth
		self.unpatch_synth()
		result = orig(*args, **kwargs)
		self.patch_synth()
		return result

	def playWaveFile(self, fileName, async=True):
		self.call_callbacks('wave', fileName=fileName, async=async)
		return self.orig_playWaveFile(fileName, async=async)

	def _get_lastIndex(self, instance):
		return self.last_index_callback()

	def set_last_index_callback(self, callback):
		self.last_index_callback = callback
