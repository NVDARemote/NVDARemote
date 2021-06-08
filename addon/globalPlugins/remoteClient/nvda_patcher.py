from . import callback_manager
import tones
import nvwave
import speech
import inputCore
import braille
import brailleInput
import scriptHandler

class NVDAPatcher(callback_manager.CallbackManager):
	"""Base class to manage patching of braille display changes."""

	def __init__(self):
		super().__init__()
		self.orig_setDisplayByName = None

	def patch_set_display(self):
		if self.orig_setDisplayByName is not None:
			return
		self.orig_setDisplayByName = braille.handler.setDisplayByName
		braille.handler.setDisplayByName = self.setDisplayByName

	def unpatch_set_display(self):
		if self.orig_setDisplayByName is None:
			return
		braille.handler.setDisplayByName = self.orig_setDisplayByName
		self.orig_setDisplayByName = None

	def patch(self):
		self.patch_set_display()

	def unpatch(self):
		self.unpatch_set_display()

	def setDisplayByName(self, *args, **kwargs):
		result=self.orig_setDisplayByName(*args, **kwargs)
		if result:
			self.call_callbacks('set_display')
		return result

class NVDASlavePatcher(NVDAPatcher):
	"""Class to manage patching of synth, tones, nvwave, and braille."""

	def __init__(self):
		super().__init__()
		self.orig_speak = None
		self.orig_cancel = None
		self.orig_beep = None
		self.orig_playWaveFile = None
		self.orig_display = None

	def patch_speech(self):
		if self.orig_speak  is not None:
			return
		self.orig_speak = speech._manager.speak
		speech._manager.speak = self.speak
		self.orig_cancel = speech._manager.cancel
		speech._manager.cancel = self.cancel

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

	def patch_braille(self):
		if self.orig_display is not None:
			return
		self.orig_display = braille.handler._writeCells
		braille.handler._writeCells = self.display

	def unpatch_speech(self):
		if self.orig_speak  is None:
			return
		speech._manager.speak = self.orig_speak
		self.orig_speak = None
		speech._manager.cancel = self.orig_cancel
		self.orig_cancel = None

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

	def unpatch_braille(self):
		if self.orig_display is None:
			return
		braille.handler._writeCells = self.orig_display
		self.orig_display = None
		braille.handler.displaySize=braille.handler.display.numCells
		braille.handler.enabled = bool(braille.handler.displaySize)

	def patch(self):
		super().patch()
		self.patch_speech()
		self.patch_tones()
		self.patch_nvwave()
		self.patch_braille()

	def unpatch(self):
		super().unpatch()
		self.unpatch_speech()
		self.unpatch_tones()
		self.unpatch_nvwave()
		self.unpatch_braille()

	def speak(self, speechSequence, priority):
		self.call_callbacks('speak', speechSequence=speechSequence, priority=priority)
		self.orig_speak(speechSequence, priority)

	def cancel(self):
		self.call_callbacks('cancel_speech')
		self.orig_cancel()

	def beep(self, hz, length, left=50, right=50):
		self.call_callbacks('beep', hz=hz, length=length, left=left, right=right)
		return self.orig_beep(hz=hz, length=length, left=left, right=right)

	def playWaveFile(self, fileName, asynchronous=True):
		"""Intercepts playing of 'wave' file.
		Used to instruct master to play this file also. File is then played locally.
		Note: Signature must match nvwave.playWaveFile
		"""
		self.call_callbacks('wave', fileName=fileName, asynchronous=asynchronous)
		return self.orig_playWaveFile(fileName, asynchronous)

	def display(self, cells):
		self.call_callbacks('display', cells=cells)
		self.orig_display(cells)

class NVDAMasterPatcher(NVDAPatcher):
	"""Class to manage patching of braille input."""

	def __init__(self):
		super().__init__()
		self.orig_executeGesture = None

	def patch_braille_input(self):
		if self.orig_executeGesture is not None:
			return
		self.orig_executeGesture = inputCore.manager.executeGesture
		inputCore.manager.executeGesture= self.executeGesture

	def unpatch_braille_input(self):
		if self.orig_executeGesture is None:
			return
		inputCore.manager.executeGesture = self.orig_executeGesture
		self.orig_executeGesture = None

	def patch(self):
		super().patch()
		# We do not patch braille input by default

	def unpatch(self):
		super().unpatch()
		# To be sure, unpatch braille input
		self.unpatch_braille_input()

	def executeGesture(self, gesture):
		if isinstance(gesture,(braille.BrailleDisplayGesture,brailleInput.BrailleInputGesture)):
			dict = { key: gesture.__dict__[key] for key in gesture.__dict__ if isinstance(gesture.__dict__[key],(int,str,bool))}
			if gesture.script:
				name=scriptHandler.getScriptName(gesture.script)
				if name.startswith("kb"):
					location=['globalCommands', 'GlobalCommands']
				else:
					location=scriptHandler.getScriptLocation(gesture.script).rsplit(".",1)
				dict["scriptPath"]=location+[name]
			else:
				scriptData=None
				maps=[inputCore.manager.userGestureMap,inputCore.manager.localeGestureMap]
				if braille.handler.display.gestureMap:
					maps.append(braille.handler.display.gestureMap)
				for map in maps:
					for identifier in gesture.identifiers:
						try:
							scriptData=next(map.getScriptsForGesture(identifier))
							break
						except StopIteration:
							continue
				if scriptData:
					dict["scriptPath"]=[scriptData[0].__module__,scriptData[0].__name__,scriptData[1]]
			if hasattr(gesture,"source") and "source" not in dict:
				dict["source"]=gesture.source
			if hasattr(gesture,"model") and "model" not in dict:
				dict["model"]=gesture.model
			if hasattr(gesture,"id") and "id" not in dict:
				dict["id"]=gesture.id
			elif hasattr(gesture,"identifiers") and "identifiers" not in dict:
				dict["identifiers"]=gesture.identifiers
			if hasattr(gesture,"dots") and "dots" not in dict:
				dict["dots"]=gesture.dots
			if hasattr(gesture,"space") and "space" not in dict:
				dict["space"]=gesture.space
			if hasattr(gesture,"routingIndex") and "routingIndex" not in dict:
				dict["routingIndex"]=gesture.routingIndex
			self.call_callbacks('braille_input', **dict)
		else:
			self.orig_executeGesture(gesture)
