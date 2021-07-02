import collections.abc
import time
import tones
import threading

local_beep = tones.beep

def beep_sequence(*sequence):
	"""	Play a simple synchronous monophonic beep sequence
	A beep sequence is an iterable containing one of two kinds of elements.
	An element consisting of a tuple of two items is interpreted as a frequency and duration. Note, this function plays beeps synchronously, unlike tones.beep
	A single integer is assumed to be a delay in ms.
	"""
	for element in sequence:
		if not isinstance(element, collections.abc.Sequence):
			time.sleep(element / 1000)
		else:
			tone, duration = element
			time.sleep(duration / 1000)
			local_beep(tone, duration)

def beep_sequence_async(*sequence):
	"""Play an asynchronous beep sequence.
	This is the same as beep_sequence, except it runs in a thread."""
	thread = threading.Thread(target=beep_sequence, args=sequence)
	thread.daemon = True
	thread.start()
