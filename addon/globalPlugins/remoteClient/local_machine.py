import ctypes
import os

import api
import braille
import inputCore
import nvwave
import speech
import tones
import versionInfo
import wx

from . import cues, input

try:
	from systemUtils import hasUiAccess
except ModuleNotFoundError:
	from config import hasUiAccess

import logging

import ui
import versionInfo

logger = logging.getLogger('local_machine')


def setSpeechCancelledToFalse():
	"""
	This function updates the state of speech so that it is aware that future
	speech should not be cancelled. In the long term this is a fragile solution
	as NVDA does not support modifying the internal state of speech.
	"""
	if versionInfo.version_year >= 2021:
		# workaround as beenCanceled is readonly as of NVDA#12395
		speech.speech._speechState.beenCanceled = False
	else:
		speech.beenCanceled = False


class LocalMachine:

	def __init__(self):
		self.isMuted = False
		self.receivingBraille=False
		self._cachedSizes = None
		if versionInfo.version_year >= 2023:
			braille.decide_enabled.register(self.handleDecideEnabled)

	def terminate(self):
		if versionInfo.version_year >= 2023:
			braille.decide_enabled.unregister(self.handleDecideEnabled)

	def playWave(self, fileName):
		"""Instructed by remote machine to play a wave file."""
		if self.isMuted:
			return
		if os.path.exists(fileName):
			# ignore async / asynchronous from kwargs:
			# playWaveFile should play asynchronously from NVDA remote.
			nvwave.playWaveFile(fileName=fileName, asynchronous=True)

	def beep(self, hz, length, left, right, **kwargs):
		if self.isMuted:
			return
		tones.beep(hz, length, left, right)

	def cancelSpeech(self, **kwargs):
		if self.isMuted:
			return
		wx.CallAfter(speech._manager.cancel)

	def pauseSpeech(self, switch, **kwargs):
		if self.isMuted:
			return
		wx.CallAfter(speech.pauseSpeech, switch)

	def speak(
			self,
			sequence,
			priority=speech.priorities.Spri.NORMAL,
			**kwargs
	):
		if self.isMuted:
			return
		setSpeechCancelledToFalse()
		wx.CallAfter(speech._manager.speak, sequence, priority)

	def display(self, cells, **kwargs):
		if self.receivingBraille and braille.handler.displaySize > 0 and len(cells) <= braille.handler.displaySize:
			# We use braille.handler._writeCells since this respects thread safe displays and automatically falls back to noBraille if desired
			cells = cells + [0] * (braille.handler.displaySize - len(cells))
			wx.CallAfter(braille.handler._writeCells, cells)

	def brailleInput(self, **kwargs):
		try:
			inputCore.manager.executeGesture(input.BrailleInputGesture(**kwargs))
		except inputCore.NoInputGestureAction:
			pass

	def setBrailleDisplay_size(self, sizes, **kwargs):
		if versionInfo.version_year >= 2023:
			self._cachedSizes = sizes
			return
		sizes.append(braille.handler.display.numCells)
		try:
			size=min(i for i in sizes if i>0)
		except ValueError:
			size = braille.handler.display.numCells
		braille.handler.displaySize = size
		braille.handler.enabled = bool(size)

	def handleFilterDisplaySize(self, value):
		if not self._cachedSizes:
			return value
		sizes = self._cachedSizes + [value]
		try:
			return min(i for i in sizes if i>0)
		except ValueError:
			return value

	def handleDecideEnabled(self):
		return not self.receivingBraille

	def sendKey(self, vk_code=None, extended=None, pressed=None, **kwargs):
		wx.CallAfter(input.send_key, vk_code, None, extended, pressed)

	def setClipboardText(self, text, **kwargs):
		cues.clipboard_received()
		api.copyToClip(text=text)

	def sendSAS(self, **kwargs):
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
