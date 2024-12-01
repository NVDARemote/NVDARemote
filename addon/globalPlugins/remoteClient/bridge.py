from typing import Any, Set, Union
from enum import Enum
from .protocol import RemoteMessageType
from .transport import Transport


class BridgeTransport:
	"""Object to bridge two transports together,
	passing messages to both of them.
	We exclude transport-specific messages such as client_joined."""
	excluded: Set[str] = {'client_joined', 'client_left', 'channel_joined', 'set_braille_info'}

	t1: Transport 
	t2: Transport

	def __init__(self, t1: Transport, t2: Transport) -> None:
		self.t1 = t1
		self.t2 = t2
		for messageType in RemoteMessageType:
			t1.registerInbound(messageType, self.send_to_t2)
			t2.registerInbound(messageType, self.send_to_t1)

	def send(self, transport: Transport, callback: Union[str, Enum], *args: Any, **kwargs: Any) -> None:
		if isinstance(callback, Enum):
			callback = callback.value
		if callback in self.excluded:
			return
		transport.send(callback, *args, **kwargs)

	def send_to_t2(self, callback, *args, **kwargs):
		self.send(self.t2, callback, *args, **kwargs)

	def send_to_t1(self, callback, *args, **kwargs):
		self.send(self.t1, callback, *args, **kwargs)

	def disconnect(self):
		for messageType in RemoteMessageType:
			self.t1.unregisterInbound(messageType, self.send_to_t2)
			self.t2.unregisterInbound(messageType, self.send_to_t1)
