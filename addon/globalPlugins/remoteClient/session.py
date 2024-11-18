
import hashlib
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import addonHandler
import braille
import gui
import speech
import ui
import versionInfo
from logHandler import log

from . import configuration, connection_info, cues, extensionMapper, local_machine
from .protocol import RemoteMessageType
from .transport import RelayTransport 


addonHandler.initTranslation()


EXCLUDED_SPEECH_COMMANDS = (
	speech.commands.BaseCallbackCommand,
	# _CancellableSpeechCommands are not designed to be reported and are used internally by NVDA. (#230)
		speech.commands._CancellableSpeechCommand,
)


class RemoteSession:
	"""Base class for a session that runs on either the master or slave machine."""

	transport: RelayTransport
	localMachine: local_machine.LocalMachine
	mode: Optional[str] = None
	extensionMapper: Optional[extensionMapper.RemoteExtensionMapper]

	def __init__(self, localMachine: local_machine.LocalMachine, transport: RelayTransport) -> None:
		self.localMachine = localMachine
		self.extensionMapper = None
		self.transport = transport
		self.transport.registerInbound(RemoteMessageType.version_mismatch, self.handleVersionMismatch)
		self.transport.registerInbound(RemoteMessageType.motd, self.handleMotd)

	def handleVersionMismatch(self) -> None:
		# translators: Message for version mismatch
		message = _("""The version of the relay server which you have connected to is not compatible with this version of the Remote Client.
Please either use a different server or upgrade your version of the addon.""")
		ui.message(message)
		self.transport.close()

	def handleMotd(self, motd: str, force_display=False):
		if force_display or self.shouldDisplayMotd(motd):
			gui.messageBox(parent=gui.mainFrame, caption=_(
				"Message of the Day"), message=motd)

	def shouldDisplayMotd(self, motd: str) -> bool:
		conf = configuration.get_config()
		host, port = self.transport.address
		host = host.lower()
		address = '{host}:{port}'.format(host=host, port=port)
		motdBytes = motd.encode('utf-8', errors='surrogatepass')
		hashed = hashlib.sha1(motdBytes).hexdigest()
		current = conf['seen_motds'].get(address, "")
		if current == hashed:
			return False
		conf['seen_motds'][address] = hashed
		conf.write()
		return True

	def getConnectionInfo(self) -> connection_info.ConnectionInfo:
		hostname, port = self.transport.address
		key = self.transport.channel
		return connection_info.ConnectionInfo(hostname=hostname, port=port, key=key, mode=self.mode)


class SlaveSession(RemoteSession):
	"""Session that runs on the slave and manages state."""

	mode: connection_info.ConnectionMode = connection_info.ConnectionMode.SLAVE
	extensionMapper: extensionMapper.SlaveExtensionMapper
	masters: Dict[int, Dict[str, Any]]
	masterDisplaySizes: List[int]
	extensionsRegistered: bool

	def __init__(self, localMachine: local_machine.LocalMachine, transport: RelayTransport) -> None:
		super().__init__(localMachine, transport)
		self.transport.registerInbound(RemoteMessageType.client_joined, self.handleClientConnected)
		self.transport.registerInbound(RemoteMessageType.client_left, self.handleClientDisconnected)
		self.transport.registerInbound(RemoteMessageType.key, self.localMachine.sendKey)
		self.masters = defaultdict(dict)
		self.masterDisplaySizes = []
		self.transport.registerInbound(RemoteMessageType.index, self.recvIndex)
		self.transport.transportClosing.register(self.handleTransportClosing)
		self.extensionMapper = extensionMapper.SlaveExtensionMapper(self.transport)
		self.extensionsRegistered = False
		self.transport.registerInbound(RemoteMessageType.channel_joined, self.handleChannelJoined)
		self.transport.registerInbound(RemoteMessageType.set_clipboard_text, self.localMachine.setClipboardText)
		self.transport.registerInbound(RemoteMessageType.set_braille_info, self.handleBrailleInfo)
		self.transport.registerInbound(RemoteMessageType.set_display_size, self.setDisplaySize)
		braille.filter_displaySize.register(
			self.localMachine.handleFilterDisplaySize)
		self.transport.registerInbound(RemoteMessageType.braille_input, self.localMachine.brailleInput)
		self.transport.registerInbound(RemoteMessageType.send_SAS, self.localMachine.sendSAS)

	def handleClientConnected(self, client: Optional[Dict[str, Any]] = None) -> None:
		self.extensionMapper.registerExtensionPoints()
		if not self.extensionsRegistered:
			self.addMapperCallbacks()
			self.extensionsRegistered = True
		cues.client_connected()
		if client['connection_type'] == 'master':
			self.masters[client['id']]['active'] = True

	def handleChannelJoined(self, channel: Optional[str] = None, clients: Optional[List[Dict[str, Any]]] = None, origin: Optional[int] = None) -> None:
		if clients is None:
			clients = []
		for client in clients:
			self.handleClientConnected(client)

	def handleTransportClosing(self) -> None:
		self.extensionMapper.unregisterExtensionPoints()
		if self.extensionsRegistered:
			self.removeMapperCallbacks()
			self.extensionsRegistered = False

	def handleTransportDisconnected(self):
		cues.client_connected()
		self.extensionMapper.unregisterExtensionPoints()

	def handleClientDisconnected(self, client=None):
		cues.client_disconnected()
		if client['connection_type'] == 'master':
			del self.masters[client['id']]
		if not self.masters:
			self.extensionMapper.unregisterExtensionPoints()

	def setDisplaySize(self, sizes=None):
		self.masterDisplaySizes = sizes if sizes else [
			info.get("braille_numCells", 0) for info in self.masters.values()]
		self.localMachine.setBrailleDisplay_size(self.masterDisplaySizes)

	def handleBrailleInfo(self, name: Optional[str] = None, numCells: int = 0, origin: Optional[int] = None) -> None:
		if not self.masters.get(origin):
			return
		self.masters[origin]['braille_name'] = name
		self.masters[origin]['braille_numCells'] = numCells
		self.setDisplaySize()

	def _getMapperCallbacks(self) -> List[Tuple[str, Callable[..., Any]]]:
		return (
			('speak', self.speak),
			('pause_speech', self.pauseSpeech),
			('display', self.display),
			('set_display', self.setDisplaySize)
		)

	def addMapperCallbacks(self) -> None:
		mapperCallbacks = self._getMapperCallbacks()
		for event, callback in mapperCallbacks:
			self.extensionMapper.registerCallback(event, callback)

	def removeMapperCallbacks(self):
		mapperCallbacks = self._getMapperCallbacks()
		for event, callback in mapperCallbacks:
			self.extensionMapper.unregisterCallback(event, callback)

	def _filterUnsupportedSpeechCommands(self, speechSequence: List[Any]) -> List[Any]:
		return list([
			item for item in speechSequence
			if not isinstance(item, EXCLUDED_SPEECH_COMMANDS)
		])

	def speak(self, speechSequence: List[Any], priority: Optional[str]) -> None:
		self.transport.send(
			type=RemoteMessageType.speak,
			sequence=self._filterUnsupportedSpeechCommands(speechSequence),
			priority=priority
		)

	def pauseSpeech(self, switch):
		self.transport.send(type=RemoteMessageType.pause_speech, switch=switch)

	def display(self, cells):
		# Only send braille data when there are controlling machines with a braille display
		if self.hasBrailleMasters():
			self.transport.send(type=RemoteMessageType.display, cells=cells)

	def hasBrailleMasters(self):
		return bool([i for i in self.masterDisplaySizes if i > 0])

	def recvIndex(self, index=None):
		pass  # speech index approach changed in 2019.3


class MasterSession(RemoteSession):

	mode: connection_info.ConnectionMode = connection_info.ConnectionMode.MASTER
	extensionMapper: extensionMapper.MasterExtensionMapper
	slaves: Dict[int, Dict[str, Any]]
	extensionsRegistered: bool

	def __init__(self, localMachine: local_machine.LocalMachine, transport: RelayTransport) -> None:
		super().__init__(localMachine, transport)
		self.slaves = defaultdict(dict)
		self.extensionMapper = extensionMapper.MasterExtensionMapper(transport=self.transport)
		self.extensionsRegistered = False
		self.transport.registerInbound(RemoteMessageType.speak, self.localMachine.speak)
		self.transport.registerInbound(RemoteMessageType.cancel, self.localMachine.cancelSpeech)
		self.transport.registerInbound(RemoteMessageType.pause_speech, self.localMachine.pauseSpeech)
		self.transport.registerInbound(RemoteMessageType.tone, self.localMachine.beep)
		self.transport.registerInbound(RemoteMessageType.wave, self.handlePlayWave)
		self.transport.registerInbound(RemoteMessageType.display, self.localMachine.display)
		self.transport.registerInbound(RemoteMessageType.nvda_not_connected, self.handleNVDANotConnected)
		self.transport.registerInbound(RemoteMessageType.client_joined, self.handleClientConnected)
		self.transport.registerInbound(RemoteMessageType.client_left, self.handleClientDisconnected)
		self.transport.registerInbound(RemoteMessageType.channel_joined, self.handleChannel_joined)
		self.transport.registerInbound(RemoteMessageType.set_clipboard_text, self.localMachine.setClipboardText)
		self.transport.registerInbound(RemoteMessageType.set_braille_info, self.sendBrailleInfo)
		self.transport.transportConnected.register(self.handleConnected)
		self.transport.transportDisconnected.register(self.handleDisconnected)

	def handlePlayWave(self, **kwargs):
		"""Receive instruction to play a 'wave' from the slave machine
		This method handles translation (between versions of NVDA Remote) of arguments required for 'msg_wave'
		"""
		# Note:
		# Version 2.2 will send only 'async' in kwargs
		# Version 2.3 will send 'asynchronous' and 'async' in kwargs
		if "fileName" not in kwargs:
			log.error("'fileName' missing from kwargs.")
			return
		fileName = kwargs.pop("fileName")
		self.localMachine.playWave(fileName=fileName)

	def handleNVDANotConnected(self) -> None:
		speech.cancelSpeech()
		ui.message(_("Remote NVDA not connected."))

	def handleConnected(self):
		# speech index approach changed in 2019.3
		pass  # nothing to do

	def handleDisconnected(self):
		# speech index approach changed in 2019.3
		pass  # nothing to do

	def handleChannel_joined(self, channel: Optional[str] = None, clients: Optional[List[Dict[str, Any]]] = None, origin: Optional[int] = None) -> None:
		if clients is None:
			clients = []
		for client in clients:
			self.handleClientConnected(client)

	def handleClientConnected(self, client=None):
		self.extensionMapper.registerExtensionPoints()
		if not self.extensionsRegistered:
			self.addMapperCallbacks()
			self.extensionsRegistered = True
		self.sendBrailleInfo()
		cues.client_connected()

	def handleClientDisconnected(self, client=None):
		self.extensionMapper.unregisterExtensionPoints()
		if self.extensionsRegistered:
			self.removeMapperCallbacks()
			self.extensionsRegistered = False
		cues.client_disconnected()

	def sendBrailleInfo(self, display: Optional[Any] = None, displaySize: Optional[int] = None) -> None:
		if display is None:
			display = braille.handler.display
		if displaySize is None:
			displaySize = braille.handler.displaySize
		self.transport.send(type=RemoteMessageType.set_braille_info,
							name=display.name, numCells=displaySize)

	def brailleInput(self) -> None:
		self.transport.send(type=RemoteMessageType.braille_input)

	def addMapperCallbacks(self):
		patcher_callbacks = (('braille_input', self.brailleInput), ('set_display', self.sendBrailleInfo))
		for event, callback in patcher_callbacks:
			self.extensionMapper.registerCallback(event, callback)

	def removeMapperCallbacks(self):
		mapperCallbacks = (('braille_input', self.brailleInput),
							 ('set_display', self.sendBrailleInfo))
		for event, callback in mapperCallbacks:
			self.extensionMapper.unregisterCallback(event, callback)
