import os

import wx
from . import input
import api
import nvwave
import tones
import speech
import ctypes
import braille
import inputCore

try:
	from systemUtils import hasUiAccess
except ModuleNotFoundError:
	from config import hasUiAccess
	
import ui
import versionInfo
import logging
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
		self.is_muted = False
		self.receiving_braille=False

	def play_wave(self, fileName):
		"""Instructed by remote machine to play a wave file."""
		if self.is_muted:
			return
		if os.path.exists(fileName):
			# ignore async / asynchronous from kwargs:
			# playWaveFile should play asynchronously from NVDA remote.
			nvwave.playWaveFile(fileName=fileName, asynchronous=True)

	def beep(self, hz, length, left, right, **kwargs):
		if self.is_muted:
			return
		tones.beep(hz, length, left, right)

	def cancel_speech(self, **kwargs):
		if self.is_muted:
			return
		wx.CallAfter(speech._manager.cancel)

	def speak(
			self,
			sequence,
			priority=speech.priorities.Spri.NORMAL,
			**kwargs
	):
		if self.is_muted:
			return
		setSpeechCancelledToFalse()
		wx.CallAfter(speech._manager.speak, sequence, priority)

	def display(self, cells, **kwargs):
		if self.receiving_braille and braille.handler.displaySize > 0 and len(cells) <= braille.handler.displaySize:
			# We use braille.handler._writeCells since this respects thread safe displays and automatically falls back to noBraille if desired
			cells = cells + [0] * (braille.handler.displaySize - len(cells))
			wx.CallAfter(braille.handler._writeCells, cells)

	def braille_input(self, **kwargs):
		try:
			inputCore.manager.executeGesture(input.BrailleInputGesture(**kwargs))
		except inputCore.NoInputGestureAction:
			pass

	def set_braille_display_size(self, sizes, **kwargs):
		sizes.append(braille.handler.display.numCells)
		try:
			size=min(i for i in sizes if i>0)
		except ValueError:
			size = braille.handler.display.numCells
		braille.handler.displaySize = size
		braille.handler.enabled = bool(size)

	def send_key(self, vk_code=None, extended=None, pressed=None, **kwargs):
		wx.CallAfter(input.send_key, vk_code, None, extended, pressed)

	def set_clipboard_text(self, text, **kwargs):
		api.copyToClip(text=text)

	def send_SAS(self, **kwargs):
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
