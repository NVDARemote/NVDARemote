from . import beep_sequence
import tones

def connected();
	beep_sequence.beep_sequence_async((440, 60), (660, 60))

def disconnected():
	beep_sequence.beep_sequence_async((660, 60), (440, 60))

def control_server_connected():
	beep_sequence.beep_sequence_async((720, 100), 50, (720, 100), 50, (720, 100))

def client_connected():
	tones.beep(1000, 300)

def client_disconnected():
	tones.beep(108, 300)

