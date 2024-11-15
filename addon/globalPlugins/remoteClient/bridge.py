from typing import Any, Set, Union
from enum import Enum
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
		t1.callback_manager.registerCallback('*', self.send_to_t2)
		t2.callback_manager.registerCallback('*', self.send_to_t1)

	def send(self, transport: Transport, callback: Union[str, Enum], *args: Any, **kwargs: Any) -> None:
		if isinstance(callback, Enum):
			callback = callback.value
		if not callback.startswith('msg_'):
			return
		msg = callback.split('_', 1)[-1]
		if msg in self.excluded:
			return
		transport.send(msg, *args, **kwargs)

	def send_to_t2(self, callback, *args, **kwargs):
		self.send(self.t2, callback, *args, **kwargs)

	def send_to_t1(self, callback, *args, **kwargs):
		self.send(self.t1, callback, *args, **kwargs)

	def disconnect(self):
		self.t1.callback_manager.unregisterCallback('*', self.send_to_t2)
		self.t2.callback_manager.unregisterCallback('*', self.send_to_t1)
