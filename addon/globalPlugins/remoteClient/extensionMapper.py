from typing import Any, Dict, List, Optional, Type, Union

import braille
import brailleInput
import inputCore
import nvwave
import scriptHandler
import speech
import tones
from speech.extensions import speechCanceled

from . import callback_manager
from .protocol import RemoteMessageType
from .transport import RelayTransport


class RemoteExtensionMapper(callback_manager.CallbackManager):
	"""Base class to manage forwarding of extension points to a remote client."""

	def __init__(self, transport: RelayTransport) -> None:
		super().__init__()
		self.transport: RelayTransport = transport
		self._registeredExtensions = {}

	def registerOutgoing(self, extensionPoint, messageType: RemoteMessageType, argument_transformer: callable = None, returnValue: Any = None):
		"""Register an NVDA extension point to forward as a remote message

		@param extension_point: The NVDA extension point to register
		@param message_type: The message type to send to the remote client
		@param transform: An optional function to transform the arguments before sending
		@param returnValue: An optional value to return to the caller of the extension point (return True for deciders)
		"""
		if argument_transformer is None:
			argument_transformer = lambda *args, **kwargs: kwargs
		def handler(*args, **kwargs):
			self.transport.send(messageType, argument_transformer(*args, **kwargs))
			return returnValue
		extensionPoint.register(handler)
		self._registeredExtensions[extensionPoint] = handler
	
	def unregisterOutgoing(self, extension_point):
		"""Unregister an NVDA extension point
		@param extension_point: The NVDA extension point to unregister  
		"""
		if extension_point in self._registeredExtensions:
			handler = self._registeredExtensions[extension_point]
			extension_point.unregister(handler)
			del self._registeredExtensions[extension_point]

	def unregister_all(self):
		"""Unregister all extension points"""
		for extension_point in list(self._registeredExtensions.keys()):
			self.unregisterOutgoing(extension_point)

	def RegisterSetDisplay(self) -> None:
		braille.displayChanged.register(self.handle_displayChanged)
		braille.displaySizeChanged.register(self.handle_displaySizeChanged)

	def unregisterSetDisplay(self) -> None:
		braille.displaySizeChanged.unregister(self.handle_displaySizeChanged)
		braille.displayChanged.unregister(self.handle_displayChanged)

	def registerExtensionPoints(self) -> None:
		self.RegisterSetDisplay()

	def unregisterExtensionPoints(self) -> None:
		self.unregisterSetDisplay()

	def handle_displayChanged(self, display: Any) -> None:
		self.callCallbacks('set_display', display=display)

	def handle_displaySizeChanged(self, displaySize: Any) -> None:
		self.callCallbacks('set_display', displaySize=displaySize)


class SlaveExtensionMapper(RemoteExtensionMapper):
	"""Class to manage patching of synth, tones, nvwave, and braille."""

	def __init__(self, transport: RelayTransport) -> None:
		super().__init__(transport=transport)
		self.origSpeak: Optional[Any] = None
		self.orig_pauseSpeech: Optional[Any] = None

	def patchSpeech(self) -> None:
		if self.origSpeak is not None:
			return
		self.origSpeak = speech._manager.speak
		speech._manager.speak = self.speak
		self.orig_pauseSpeech = speech.pauseSpeech
		speech.pauseSpeech = self.pauseSpeech

	def registerBraille(self) -> None:
		braille.pre_writeCells.register(self.handle_pre_writeCells)

	def unpatchSpeech(self):
		if self.origSpeak is None:
			return
		speech._manager.speak = self.origSpeak
		self.origSpeak = None
		speech.pauseSpeech = self.orig_pauseSpeech
		self.orig_pauseSpeech = None

	def unregisterBraille(self):
		braille.pre_writeCells.unregister(self.handle_pre_writeCells)

	def registerExtensionPoints(self):
		self.patchSpeech()
		self.registerOutgoing(extensionPoint=speechCanceled, messageType=RemoteMessageType.speech_canceled)
		self.registerOutgoing(extensionPoint=tones.decide_beep, messageType=RemoteMessageType.tone, returnValue=True)
		self.registerOutgoing(extensionPoint=nvwave.decide_playWaveFile, messageType=RemoteMessageType.wave, returnValue=True, argument_transformer=self.transformPlayWave)
		self.registerBraille()

	@staticmethod
	def transformPlayWave(**kwargs):
		"""This machine played a sound, send it to Master machine"""
		kwargs.update({
			# nvWave.playWaveFile should always be asynchronous when called from NVDA remote, so always send 'True'
			# Version 2.2 requires 'async' keyword.
			'async': True,
			# Version 2.3 onwards. Not currently used, but matches arguments for nvWave.playWaveFile.
			# Including it allows for forward compatibility if requirements change.
			'asynchronous': True,
		})
		return kwargs

	def unregisterExtensionPoints(self):
		self.unpatchSpeech()
		self.unregisterOutgoing(extension_point=speechCanceled)
		self.unregisterOutgoing(extension_point=tones.decide_beep)
		self.unregisterOutgoing(extension_point=nvwave.decide_playWaveFile)
		self.unregisterBraille()

	def speak(self, speechSequence: Any, priority: Any) -> None:
		self.callCallbacks(
			'speak', speechSequence=speechSequence, priority=priority)
		self.origSpeak(speechSequence, priority)

	def pauseSpeech(self, switch: bool) -> None:
		self.callCallbacks('pause_speech', switch=switch)
		self.orig_pauseSpeech(switch)

	def handle_pre_writeCells(self, cells: List[int]) -> None:
		self.callCallbacks('display', cells=cells)


class MasterExtensionMapper(RemoteExtensionMapper):
	"""Class to manage the forwarding of braille input to a remote client."""

	def registerBrailleInputHandler(self) -> None:
		inputCore.decide_executeGesture.register(
			self.handle_decide_executeGesture)

	def unregisterBrailleInputHandler(self) -> None:
		inputCore.decide_executeGesture.unregister(
			self.handle_decide_executeGesture)

	def registerExtensionPoints(self):
		super().registerExtensionPoints()
		# We do not patch braille input by default

	def unregisterExtensionPoints(self):
		super().unregisterExtensionPoints()
		# To be sure, unpatch braille input
		self.unregisterBrailleInputHandler()

	def handle_decide_executeGesture(self, gesture: Union[braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture, Any]) -> bool:
		if isinstance(gesture, (braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture)):
			dict = {key: gesture.__dict__[key] for key in gesture.__dict__ if isinstance(
				gesture.__dict__[key], (int, str, bool))}
			if gesture.script:
				name = scriptHandler.getScriptName(gesture.script)
				if name.startswith("kb"):
					location = ['globalCommands', 'GlobalCommands']
				else:
					location = scriptHandler.getScriptLocation(
						gesture.script).rsplit(".", 1)
				dict["scriptPath"] = location+[name]
			else:
				scriptData = None
				maps = [inputCore.manager.userGestureMap,
						inputCore.manager.localeGestureMap]
				if braille.handler.display.gestureMap:
					maps.append(braille.handler.display.gestureMap)
				for map in maps:
					for identifier in gesture.identifiers:
						try:
							scriptData = next(
								map.getScriptsForGesture(identifier))
							break
						except StopIteration:
							continue
				if scriptData:
					dict["scriptPath"] = [scriptData[0].__module__,
										  scriptData[0].__name__, scriptData[1]]
			if hasattr(gesture, "source") and "source" not in dict:
				dict["source"] = gesture.source
			if hasattr(gesture, "model") and "model" not in dict:
				dict["model"] = gesture.model
			if hasattr(gesture, "id") and "id" not in dict:
				dict["id"] = gesture.id
			elif hasattr(gesture, "identifiers") and "identifiers" not in dict:
				dict["identifiers"] = gesture.identifiers
			if hasattr(gesture, "dots") and "dots" not in dict:
				dict["dots"] = gesture.dots
			if hasattr(gesture, "space") and "space" not in dict:
				dict["space"] = gesture.space
			if hasattr(gesture, "routingIndex") and "routingIndex" not in dict:
				dict["routingIndex"] = gesture.routingIndex
			self.callCallbacks('braille_input', **dict)
			return False
		else:
			return True
