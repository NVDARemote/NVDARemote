from logging import getLogger
log = getLogger('serializer')
import sys
import os
try:
	import json
except ImportError:
	sys.path.append(os.path.abspath(os.path.dirname(__file__)))
	import json
	sys.path.remove(sys.path[-1])
import speech

class JSONSerializer(object):
	SEP = '\n'

	def serialize(self, type=None, **obj):
		obj['type'] = type
		data = json.dumps(obj, cls=CustomEncoder) + self.SEP
		return data

	def deserialize(self, data):
		obj = json.loads(data, object_hook=as_sequence)
		return obj


SEQUENCE_CLASSES = (speech.SpeechCommand, speech.CharacterModeCommand, speech.BreakCommand)
class CustomEncoder(json.JSONEncoder):

	def default(self, obj):
		if is_subclass_or_instance(obj, SEQUENCE_CLASSES):
			return [obj.__class__.__name__, obj.__dict__]
		return super(CustomEncoder, self).default(obj)

def is_subclass_or_instance(unknown, possible):
	try:
		return issubclass(unknown, possible)
	except TypeError:
		return isinstance(unknown, possible)

def as_sequence(dct):
	if not ('type' in dct and dct['type'] == 'speak' and 'sequence' in dct):
		return dct
	sequence = []
	for item in dct['sequence']:
		if not isinstance(item, list):
			sequence.append(item)
			continue
		name, values = item
		if not hasattr(speech, name):
			log.warning("Unknown sequence type received: %r" % name)
			continue
		cls = getattr(speech, name)
		if not issubclass(cls, SEQUENCE_CLASSES):
			log.warning("Unknown sequence type received: %r" % name)
			continue
		cls = cls.__new__(cls)
		cls.__dict__.update(values)
		sequence.append(cls)
	dct['sequence'] = sequence
	return dct
