from typing import Any, Dict, List, Optional, Union, Type
import braille
import brailleInput
import inputCore
import nvwave
import scriptHandler
import speech
from speech.extensions import speechCanceled
import tones
import versionInfo

from . import callback_manager


class NVDAPatcher(callback_manager.CallbackManager):
	"""Base class to manage patching of braille display changes."""

	def patchSetDisplay(self) -> None:
		braille.displayChanged.register(self.handle_displayChanged)
		braille.displaySizeChanged.register(self.handle_displaySizeChanged)

	def unpatchSetDisplay(self) -> None:
		braille.displaySizeChanged.unregister(self.handle_displaySizeChanged)
		braille.displayChanged.unregister(self.handle_displayChanged)

	def patch(self) -> None:
		self.patchSetDisplay()

	def unpatch(self) -> None:
		self.unpatchSetDisplay()

	def handle_displayChanged(self, display: Any) -> None:
		self.callCallbacks('set_display', display=display)

	def handle_displaySizeChanged(self, displaySize: Any) -> None:
		self.callCallbacks('set_display', displaySize=displaySize)

class NVDASlavePatcher(NVDAPatcher):
	"""Class to manage patching of synth, tones, nvwave, and braille."""

	def __init__(self) -> None:
		super().__init__()
		self.origSpeak: Optional[Any] = None
		self.orig_pauseSpeech: Optional[Any] = None

	def patchSpeech(self) -> None:
		if self.origSpeak  is not None:
			return
		self.origSpeak = speech._manager.speak
		speech._manager.speak = self.speak
		speechCanceled.register(self.cancel)
		self.orig_pauseSpeech = speech.pauseSpeech
		speech.pauseSpeech = self.pauseSpeech

	def patchTones(self) -> None:
		tones.decide_beep.register(self.handle_decide_beep)

	def patchNvwave(self) -> None:
		nvwave.decide_playWaveFile.register(self.handle_decide_playWaveFile)

	def patchBraille(self) -> None:
		braille.pre_writeCells.register(self.handle_pre_writeCells)

	def unpatchSpeech(self):
		if self.origSpeak  is None:
			return
		speech._manager.speak = self.origSpeak
		self.origSpeak = None
		speechCanceled.unregister(self.cancel)
		speech.pauseSpeech = self.orig_pauseSpeech
		self.orig_pauseSpeech = None

	def unpatchTones(self):
		tones.decide_beep.unregister(self.handle_decide_beep)

	def unpatchNvwave(self):
		nvwave.decide_playWaveFile.unregister(self.handle_decide_playWaveFile)

	def unpatchBraille(self):
		braille.pre_writeCells.unregister(self.handle_pre_writeCells)

	def patch(self):
		self.patchSpeech()
		self.patchTones()
		self.patchNvwave()
		self.patchBraille()

	def unpatch(self):
		self.unpatchSpeech()
		self.unpatchTones()
		self.unpatchNvwave()
		self.unpatchBraille()

	def speak(self, speechSequence: Any, priority: Any) -> None:
		self.callCallbacks('speak', speechSequence=speechSequence, priority=priority)
		self.origSpeak(speechSequence, priority)

	def cancel(self) -> None:
		self.callCallbacks('cancel_speech')

	def pauseSpeech(self, switch: bool) -> None:
		self.callCallbacks('pause_speech', switch=switch)
		self.orig_pauseSpeech(switch)

	def handle_decide_beep(self, hz: float, length: int, left: int = 50, right: int = 50, isSpeechBeepCommand: bool = False) -> bool:
		self.callCallbacks('beep', hz=hz, length=length, left=left, right=right, isSpeechBeepCommand=isSpeechBeepCommand)
		return True

	def handle_decide_playWaveFile(self, fileName: str, asynchronous: bool = True, isSpeechWaveFileCommand: bool = False) -> bool:
		self.callCallbacks('wave', fileName=fileName, asynchronous=asynchronous, isSpeechWaveFileCommand=isSpeechWaveFileCommand)
		return True

	def handle_pre_writeCells(self, cells: List[int]) -> None:
		self.callCallbacks('display', cells=cells)

class NVDAMasterPatcher(NVDAPatcher):
	"""Class to manage patching of braille input."""

	def patchBrailleInput(self) -> None:
		inputCore.decide_executeGesture.register(self.handle_decide_executeGesture)

	def unpatchBrailleInput(self) -> None:
		inputCore.decide_executeGesture.unregister(self.handle_decide_executeGesture)

	def patch(self):
		super().patch()
		# We do not patch braille input by default

	def unpatch(self):
		super().unpatch()
		# To be sure, unpatch braille input
		self.unpatchBrailleInput()

	def handle_decide_executeGesture(self, gesture: Union[braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture, Any]) -> bool:
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
			self.callCallbacks('braille_input', **dict)
			return False
		else:
			return True
