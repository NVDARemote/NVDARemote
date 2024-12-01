from typing import Any, Set, Dict
from enum import Enum
from .protocol import RemoteMessageType
from .transport import Transport

class BridgeTransport:
	excluded: Set[str] = {'client_joined', 'client_left', 'channel_joined', 'set_braille_info'}

	def __init__(self, t1: Transport, t2: Transport) -> None:
		self.t1 = t1
		self.t2 = t2
		# Store callbacks for each message type
		self.t1_callbacks: Dict[RemoteMessageType, callable] = {}
		self.t2_callbacks: Dict[RemoteMessageType, callable] = {}
		
		for messageType in RemoteMessageType:
			# Create and store callbacks
			self.t1_callbacks[messageType] = self.make_callback(self.t1, messageType)
			self.t2_callbacks[messageType] = self.make_callback(self.t2, messageType)
			# Register with stored references
			t1.registerInbound(messageType, self.t2_callbacks[messageType])
			t2.registerInbound(messageType, self.t1_callbacks[messageType])

	def make_callback(self, target_transport: Transport, message_type: RemoteMessageType):
		def callback(*args, **kwargs):
			if message_type.value not in self.excluded:
				target_transport.send(message_type, *args, **kwargs)
		return callback

	def disconnect(self):
		for messageType in RemoteMessageType:
			self.t1.unregisterInbound(messageType, self.t2_callbacks[messageType])
			self.t2.unregisterInbound(messageType, self.t1_callbacks[messageType])