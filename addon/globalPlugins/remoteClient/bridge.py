from typing import Any, Set, Union
from enum import Enum
from .protocol import RemoteMessageType
from .transport import Transport
from functools import partial

class BridgeTransport:
    excluded: Set[str] = {'client_joined', 'client_left', 'channel_joined', 'set_braille_info'}

    def __init__(self, t1: Transport, t2: Transport) -> None:
        self.t1 = t1
        self.t2 = t2
        # Create and store the bound methods as instance variables
        self._t1_callback = self.make_callback(self.t1)
        self._t2_callback = self.make_callback(self.t2)
        
        for messageType in RemoteMessageType:
            t1.registerInbound(messageType, self._t2_callback)
            t2.registerInbound(messageType, self._t1_callback)

    def make_callback(self, target_transport: Transport):
        def callback(message_type, *args, **kwargs):
            if message_type.value not in self.excluded:
                target_transport.send(message_type, *args, **kwargs)
        return callback

    def disconnect(self):
        for messageType in RemoteMessageType:
            self.t1.unregisterInbound(messageType, self._t2_callback)
            self.t2.unregisterInbound(messageType, self._t1_callback)