from logging import getLogger
log = getLogger('serializer')
import json
import speech.commands

class JSONSerializer:
	SEP = B'\n'

	def serialize(self, type=None, **obj) -> bytes:
		obj['type'] = type
		data = json.dumps(obj, cls=CustomEncoder).encode('UTF-8') + self.SEP
		return data

	def deserialize(self, data: bytes):
		obj = json.loads(data, object_hook=as_sequence)
		return obj


SEQUENCE_CLASSES = (
	speech.commands.SynthCommand,
	speech.commands.EndUtteranceCommand,
)

class CustomEncoder(json.JSONEncoder):

	def default(self, obj):
		if is_subclass_or_instance(obj, SEQUENCE_CLASSES):
			return [obj.__class__.__name__, obj.__dict__]
		return super().default(obj)

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
		cls = getattr(speech.commands, name, None)
		if cls is None or not issubclass(cls, SEQUENCE_CLASSES):
			log.warning("Unknown sequence type received: %r" % name)
			continue
		cls = cls.__new__(cls)
		cls.__dict__.update(values)
		sequence.append(cls)
	dct['sequence'] = sequence
	return dct
