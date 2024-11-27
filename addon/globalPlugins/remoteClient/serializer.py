from abc import abstractmethod
from enum import Enum
from logging import getLogger
from typing import Any, Dict, List, Optional, Type, Union, TypeVar
import json

import speech.commands

log = getLogger('serializer')

T = TypeVar('T')
JSONDict = Dict[str, Any]

class Serializer:

	@abstractmethod
	def serialize(self, type: Optional[str] = None, **obj: Any) -> bytes:
		raise NotImplementedError
	
	@abstractmethod
	def deserialize(self, data: bytes) -> JSONDict:
		raise NotImplementedError
	

class JSONSerializer(Serializer):
	SEP: bytes = b'\n'

	def serialize(self, type: Optional[str] = None, **obj: Any) -> bytes:
		if type is not None:
			if isinstance(type, Enum):
				type = type.value
		obj['type'] = type
		data = json.dumps(obj, cls=CustomEncoder).encode('UTF-8') + self.SEP
		return data

	def deserialize(self, data: bytes) -> JSONDict:
		obj = json.loads(data, object_hook=as_sequence)
		return obj


SEQUENCE_CLASSES = (
	speech.commands.SynthCommand,
	speech.commands.EndUtteranceCommand,
)

class CustomEncoder(json.JSONEncoder):

	def default(self, obj: Any) -> Any:
		if is_subclass_or_instance(obj, SEQUENCE_CLASSES):
			return [obj.__class__.__name__, obj.__dict__]
		return super().default(obj)

def is_subclass_or_instance(unknown: Any, possible: Union[Type[T], tuple[Type[T], ...]]) -> bool:
	try:
		return issubclass(unknown, possible)
	except TypeError:
		return isinstance(unknown, possible)

def as_sequence(dct: JSONDict) -> JSONDict:
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
