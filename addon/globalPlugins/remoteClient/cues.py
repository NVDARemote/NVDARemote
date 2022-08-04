import os
from . import beep_sequence
import tones
import nvwave
from . import configuration

local_beep = tones.beep
local_playWaveFile = nvwave.playWaveFile

def connected():
	if should_play_sounds():
		play_sound("connected")
	else:
		beep_sequence.beep_sequence_async((440, 60), (660, 60))

def disconnected():
	if should_play_sounds():
		play_sound("disconnected")
	else:
		beep_sequence.beep_sequence_async((660, 60), (440, 60))

def control_server_connected():
	if should_play_sounds():
		play_sound("controlled")
	else:
		beep_sequence.beep_sequence_async((720, 100), 50, (720, 100), 50, (720, 100))

def client_connected():
	if should_play_sounds():
		play_sound("controlling")
	else:
		local_beep(1000, 300)

def client_disconnected():
	if should_play_sounds():
		play_sound("disconnected")
	else:
		local_beep(108, 300)

def clipboard_pushed():
	if should_play_sounds():
		play_sound("push_clipboard")
	else:
		beep_sequence.beep_sequence_async((500, 100), (600, 100))

def clipboard_received():
	if should_play_sounds():
		play_sound("receive_clipboard")
	else:
		beep_sequence.beep_sequence_async((600, 100), (500, 100))

def should_play_sounds():
	return configuration.get_config()['ui']['play_sounds']

def play_sound(filename):
	path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'sounds', filename))
	return local_playWaveFile(path + ".wav")
