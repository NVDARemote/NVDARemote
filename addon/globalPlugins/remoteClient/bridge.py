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
		self.t1Callbacks: Dict[RemoteMessageType, callable] = {}
		self.t2Callbacks: Dict[RemoteMessageType, callable] = {}
		
		for messageType in RemoteMessageType:
			# Create and store callbacks
			self.t1Callbacks[messageType] = self.makeCallback(self.t1, messageType)
			self.t2Callbacks[messageType] = self.makeCallback(self.t2, messageType)
			# Register with stored references
			t1.registerInbound(messageType, self.t2Callbacks[messageType])
			t2.registerInbound(messageType, self.t1Callbacks[messageType])

	def makeCallback(self, targetTransport: Transport, messageType: RemoteMessageType):
		def callback(*args, **kwargs):
			if messageType.value not in self.excluded:
				targetTransport.send(messageType, *args, **kwargs)
		return callback

	def disconnect(self):
		for messageType in RemoteMessageType:
			self.t1.unregisterInbound(messageType, self.t2Callbacks[messageType])
			self.t2.unregisterInbound(messageType, self.t1Callbacks[messageType])