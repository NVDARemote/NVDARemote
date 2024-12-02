"""Local machine interface for NVDA Remote.

This module provides functionality for controlling the local NVDA instance
in response to commands received from remote connections. It handles:

* Speech output and cancellation
* Braille display management
* Audio playback
* Keyboard input simulation
* Clipboard operations
* System functions like Secure Attention Sequence (SAS)

The main class :class:`LocalMachine` implements all the local control operations
that can be triggered by remote NVDA instances.
"""

from typing import List, Optional, Union, Sequence, Any, Dict
import ctypes
import os
import logging

import api
import braille
import inputCore
import nvwave
import speech
import tones
import wx
from speech.types import SpeechSequence
from speech.priorities import Spri

from . import cues, input

try:
    from systemUtils import hasUiAccess
except ModuleNotFoundError:
    from config import hasUiAccess

import logging

import ui

logger = logging.getLogger('local_machine')


def setSpeechCancelledToFalse() -> None:
	"""Reset the speech cancellation flag to allow new speech.
	
	This function updates NVDA's internal speech state to ensure future
	speech will not be cancelled. This is necessary when receiving remote
	speech commands to ensure they are properly processed.
	
	Warning:
		This is a temporary workaround that modifies internal NVDA state.
		It may break in future NVDA versions if the speech subsystem changes.
	
	See Also:
		:meth:`LocalMachine.speak`
	"""
	# workaround as beenCanceled is readonly as of NVDA#12395
	speech.speech._speechState.beenCanceled = False


class LocalMachine:
	"""Controls the local NVDA instance based on remote commands.
	
	This class implements the local side of remote control functionality,
	managing speech, braille, input and other local NVDA features based on
	commands received from remote connections.
	
	The local machine can be muted to ignore remote commands, and handles
	coordination of braille display sharing between local and remote instances.
	
	Attributes:
		isMuted (bool): If True, most remote commands will be ignored
		receivingBraille (bool): If True, braille output comes from remote machine
		_cachedSizes (Optional[List[int]]): Cached braille display sizes from remote
	"""

	def __init__(self) -> None:
		"""Initialize the local machine controller.
		
		Sets up initial state and registers braille display handlers.
		The local machine starts unmuted with local braille enabled.
		"""
		self.isMuted: bool = False
		self.receivingBraille: bool = False
		self._cachedSizes: Optional[List[int]] = None
		braille.decide_enabled.register(self.handleDecideEnabled)

	def terminate(self) -> None:
		braille.decide_enabled.unregister(self.handleDecideEnabled)

	def playWave(self, fileName: str) -> None:
		"""Instructed by remote machine to play a wave file."""
		if self.isMuted:
			return
		if os.path.exists(fileName):
			# ignore async / asynchronous from kwargs:
			# playWaveFile should play asynchronously from NVDA remote.
			nvwave.playWaveFile(fileName=fileName, asynchronous=True)

	def beep(self, hz: float, length: int, left: int = 50, right: int = 50, **kwargs: Any) -> None:
		if self.isMuted:
			return
		tones.beep(hz, length, left, right)

	def cancelSpeech(self, **kwargs: Any) -> None:
		if self.isMuted:
			return
		wx.CallAfter(speech._manager.cancel)

	def pauseSpeech(self, switch: bool, **kwargs: Any) -> None:
		if self.isMuted:
			return
		wx.CallAfter(speech.pauseSpeech, switch)

	def speak(
			self,
			sequence: SpeechSequence,
			priority: Spri = Spri.NORMAL,
			**kwargs: Any
	) -> None:
		if self.isMuted:
			return
		setSpeechCancelledToFalse()
		wx.CallAfter(speech._manager.speak, sequence, priority)

	def display(self, cells: List[int], **kwargs: Any) -> None:
		if self.receivingBraille and braille.handler.displaySize > 0 and len(cells) <= braille.handler.displaySize:
			# We use braille.handler._writeCells since this respects thread safe displays and automatically falls back to noBraille if desired
			cells = cells + [0] * (braille.handler.displaySize - len(cells))
			wx.CallAfter(braille.handler._writeCells, cells)

	def brailleInput(self, **kwargs: Dict[str, Any]) -> None:
		try:
			inputCore.manager.executeGesture(input.BrailleInputGesture(**kwargs))
		except inputCore.NoInputGestureAction:
			pass

	def setBrailleDisplay_size(self, sizes: List[int], **kwargs: Any) -> None:
		self._cachedSizes = sizes

	def handleFilterDisplaySize(self, value: int) -> int:
		if not self._cachedSizes:
			return value
		sizes = self._cachedSizes + [value]
		try:
			return min(i for i in sizes if i>0)
		except ValueError:
			return value

	def handleDecideEnabled(self) -> bool:
		return not self.receivingBraille

	def sendKey(
		self,
		vk_code: Optional[int] = None,
		extended: Optional[bool] = None,
		pressed: Optional[bool] = None,
		**kwargs: Any
	) -> None:
		wx.CallAfter(input.send_key, vk_code, None, extended, pressed)

	def setClipboardText(self, text: str, **kwargs: Any) -> None:
		cues.clipboard_received()
		api.copyToClip(text=text)

	def sendSAS(self, **kwargs: Any) -> None:
		"""
		This function simulates as "a secure attention sequence" such as CTRL+ALT+DEL.
		SendSAS requires UI Access, so we provide a warning when this fails.
		This warning will only be read by the remote NVDA if it is currently connected to the machine.
		"""
		if hasUiAccess():
			ctypes.windll.sas.SendSAS(0)
		else:
			# Translators: Sent when a user fails to send CTRL+ALT+DEL from a remote NVDA instance
			ui.message(_("No permission on device to trigger CTRL+ALT+DEL from remote"))
			logger.warning("UI Access is disabled on this machine so cannot trigger CTRL+ALT+DEL")
