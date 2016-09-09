import os
import wx
import input
import api
import nvwave
import tones
import speech
import nvda_patcher
import ctypes

import logging
logger = logging.getLogger('local_machine')

class LocalMachine(object):

	def __init__(self):
		self.is_muted = False
		self.patcher = nvda_patcher.NVDAPatcher()

	def play_wave(self, fileName, async):
		if self.is_muted:
			return
		if os.path.exists(fileName):
			nvwave.playWaveFile(fileName=fileName, async=async)

	def beep(self, hz, length, left, right):
		if self.is_muted:
			return
		tones.beep(hz, length, left, right)

	def cancel_speech(self):
		if self.is_muted:
			return
		synth = speech.getSynth()
		wx.CallAfter(synth.cancel)

	def speak(self, sequence):
		if self.is_muted:
			return
		synth = speech.getSynth()
		speech.beenCanceled = False
		wx.CallAfter(synth.speak, sequence)

	def send_key(self, vk_code=None, extended=None, pressed=None, **kwargs):
		wx.CallAfter(input.send_key, vk_code, None, extended, pressed)

	def set_clipboard_text(self, text):
		api.copyToClip(text=text)

	def send_SAS(self):
		ctypes.windll.sas.SendSAS(0)
