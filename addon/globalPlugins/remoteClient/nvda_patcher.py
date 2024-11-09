import braille
import brailleInput
import inputCore
import nvwave
import scriptHandler
import speech
import tones
import versionInfo

from . import callback_manager


class NVDAPatcher(callback_manager.CallbackManager):
	"""Base class to manage patching of braille display changes."""

	def __init__(self):
		super().__init__()
		self.origSetDisplayByName = None

	def patchSetDisplay(self):
		if versionInfo.version_year >= 2023:
			braille.displayChanged.register(self.handle_displayChanged)
			braille.displaySizeChanged.register(self.handle_displaySizeChanged)
			return
		if self.origSetDisplayByName is not None:
			return
		self.origSetDisplayByName = braille.handler.setDisplayByName
		braille.handler.setDisplayByName = self.setDisplayByName

	def unpatchSetDisplay(self):
		if versionInfo.version_year >= 2023:
			braille.displaySizeChanged.unregister(self.handle_displaySizeChanged)
			braille.displayChanged.unregister(self.handle_displayChanged)
			return
		if self.origSetDisplayByName is None:
			return
		braille.handler.setDisplayByName = self.origSetDisplayByName
		self.origSetDisplayByName = None

	def patch(self):
		self.patchSetDisplay()

	def unpatch(self):
		self.unpatchSetDisplay()

	def setDisplayByName(self, *args, **kwargs):
		result=self.origSetDisplayByName(*args, **kwargs)
		if result:
			self.call_callbacks('set_display')
		return result

	def handle_displayChanged(self, display):
		self.call_callbacks('set_display', display=display)

	def handle_displaySizeChanged(self, displaySize):
		self.call_callbacks('set_display', displaySize=displaySize)

class NVDASlavePatcher(NVDAPatcher):
	"""Class to manage patching of synth, tones, nvwave, and braille."""

	def __init__(self):
		super().__init__()
		self.origSpeak = None
		self.origCancel = None
		self.origBeep = None
		self.origPlayWaveFile = None
		self.origDisplay = None

	def patchSpeech(self):
		if self.origSpeak  is not None:
			return
		self.origSpeak = speech._manager.speak
		speech._manager.speak = self.speak
		self.origCancel = speech._manager.cancel
		speech._manager.cancel = self.cancel
		self.orig_pauseSpeech = speech.pauseSpeech
		speech.pauseSpeech = self.pauseSpeech

	def patchTones(self):
		if versionInfo.version_year >= 2023:
			tones.decide_beep.register(self.handle_decide_beep)
			return
		if self.origBeep is not None:
			return
		self.origBeep = tones.beep
		tones.beep = self.beep

	def patchNvwave(self):
		if versionInfo.version_year >= 2023:
			nvwave.decide_playWaveFile.register(self.handle_decide_playWaveFile)
			return
		if self.origPlayWaveFile is not None:
			return
		self.origPlayWaveFile = nvwave.playWaveFile
		nvwave.playWaveFile = self.playWaveFile

	def patchBraille(self):
		if versionInfo.version_year >= 2023:
			braille.pre_writeCells.register(self.handle_pre_writeCells)
			return
		if self.origDisplay is not None:
			return
		self.origDisplay = braille.handler._writeCells
		braille.handler._writeCells = self.display

	def unpatchSpeech(self):
		if self.origSpeak  is None:
			return
		speech._manager.speak = self.origSpeak
		self.origSpeak = None
		speech._manager.cancel = self.origCancel
		self.origCancel = None
		speech.pauseSpeech = self.orig_pauseSpeech
		self.orig_pauseSpeech = None

	def unpatchTones(self):
		if versionInfo.version_year >= 2023:
			tones.decide_beep.unregister(self.handle_decide_beep)
			return
		if self.origBeep is None:
			return
		tones.beep = self.origBeep
		self.origBeep = None

	def unpatchNvwave(self):
		if versionInfo.version_year >= 2023:
			nvwave.decide_playWaveFile.unregister(self.handle_decide_playWaveFile)
			return
		if self.origPlayWaveFile is None:
			return
		nvwave.playWaveFile = self.origPlayWaveFile
		self.origPlayWaveFile = None

	def unpatchBraille(self):
		if versionInfo.version_year >= 2023:
			braille.pre_writeCells.unregister(self.handle_pre_writeCells)
			return
		if self.origDisplay is None:
			return
		braille.handler._writeCells = self.origDisplay
		self.origDisplay = None
		braille.handler.displaySize=braille.handler.display.numCells
		braille.handler.enabled = bool(braille.handler.displaySize)

	def patch(self):
		if versionInfo.version_year < 2023:
			super().patch()
		self.patchSpeech()
		self.patchTones()
		self.patchNvwave()
		self.patchBraille()

	def unpatch(self):
		if versionInfo.version_year < 2023:
			super().unpatch()
		self.unpatchSpeech()
		self.unpatchTones()
		self.unpatchNvwave()
		self.unpatchBraille()

	def speak(self, speechSequence, priority):
		self.call_callbacks('speak', speechSequence=speechSequence, priority=priority)
		self.origSpeak(speechSequence, priority)

	def cancel(self):
		self.call_callbacks('cancel_speech')
		self.origCancel()

	def pauseSpeech(self, switch):
		self.call_callbacks('pause_speech', switch=switch)
		self.orig_pauseSpeech(switch)

	def beep(self, hz, length, left=50, right=50):
		"""Pre NVDA 2023.1."""
		self.call_callbacks('beep', hz=hz, length=length, left=left, right=right)
		return self.origBeep(hz=hz, length=length, left=left, right=right)

	def handle_decide_beep(self, hz, length, left=50, right=50, isSpeechBeepCommand=False):
		self.call_callbacks('beep', hz=hz, length=length, left=left, right=right, isSpeechBeepCommand=isSpeechBeepCommand)
		return True

	def playWaveFile(self, fileName, asynchronous=True):
		"""Pre NVDA 2023.1.
		Intercepts playing of 'wave' file.
		Used to instruct master to play this file also. File is then played locally.
		Note: Signature must match nvwave.playWaveFile
		"""
		self.call_callbacks('wave', fileName=fileName, asynchronous=asynchronous)
		return self.origPlayWaveFile(fileName, asynchronous)

	def handle_decide_playWaveFile(self, fileName, asynchronous=True, isSpeechWaveFileCommand=False):
		self.call_callbacks('wave', fileName=fileName, asynchronous=asynchronous, isSpeechWaveFileCommand=isSpeechWaveFileCommand)
		return True

	def display(self, cells):
		self.handle_pre_writeCells(cells=cells)
		self.origDisplay(cells)

	def handle_pre_writeCells(self, cells):
		self.call_callbacks('display', cells=cells)

class NVDAMasterPatcher(NVDAPatcher):
	"""Class to manage patching of braille input."""

	def __init__(self):
		super().__init__()
		self.orig_ExecuteGesture = None

	def patch_Braille_input(self):
		if versionInfo.version_year >= 2023:
			inputCore.decide_executeGesture.register(self.handle_decide_executeGesture)
			return
		if self.orig_ExecuteGesture is not None:
			return
		self.orig_ExecuteGesture = inputCore.manager.executeGesture
		inputCore.manager.executeGesture= self.executeGesture

	def unpatchBraille_input(self):
		if versionInfo.version_year >= 2023:
			inputCore.decide_executeGesture.unregister(self.handle_decide_executeGesture)
			return
		if self.orig_ExecuteGesture is None:
			return
		inputCore.manager.executeGesture = self.orig_ExecuteGesture
		self.orig_ExecuteGesture = None

	def patch(self):
		super().patch()
		# We do not patch braille input by default

	def unpatch(self):
		super().unpatch()
		# To be sure, unpatch braille input
		self.unpatchBraille_input()

	def handle_decide_executeGesture(self, gesture):
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
			return False
		else:
			return True

	def executeGesture(self, gesture):
		if not self.handle_decide_executeGesture(gesture):
			self.orig_ExecuteGesture(gesture)
