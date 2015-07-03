from __future__ import division
import collections
import time
import tones

def beep_sequence(*sequence):
	"""	Play a simple synchronous monophonic beep sequence
	A beep sequence is an iterable containing one of two kinds of elements.
	An element consisting of a tuple of two items is interpreted as a frequency and duration. Note, this function plays beeps synchronously, unlike tones.beep
	A single integer is assumed to be a delay in ms.
	"""
	for element in sequence:
		if not isinstance(element, collections.Sequence):
			time.sleep(element / 1000)
		else:
			tone, duration = element
			time.sleep(duration / 1000)
			tones.beep(tone, duration)
