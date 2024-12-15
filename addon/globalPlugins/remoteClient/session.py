import hashlib
from collections import defaultdict
from typing import Dict, List, Optional, Tuple, Any, Callable


import addonHandler
import braille
import gui
import nvwave
import speech
import tones
import ui
from speech.extensions import speechCanceled

from . import configuration, connection_info, cues, local_machine, nvda_patcher

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
	mode: Optional[connection_info.ConnectionMode] = None
	patcher: Optional[nvda_patcher.NVDAPatcher]
	patchCallbacksAdded: bool

	def __init__(
		self, localMachine: local_machine.LocalMachine, transport: RelayTransport
	) -> None:
		self.localMachine = localMachine
		self.patcher = None
		self.patchCallbacksAdded = False
		self.transport = transport
		self.transport.registerInbound(
			RemoteMessageType.version_mismatch, self.handleVersionMismatch
		)
		self.transport.registerInbound(RemoteMessageType.motd, self.handleMOTD)
		self.transport.registerInbound(
			RemoteMessageType.set_clipboard_text, self.localMachine.setClipboardText
		)
		self.transport.registerInbound(
			RemoteMessageType.client_joined, self.handleClientConnected
		)
		self.transport.registerInbound(
			RemoteMessageType.client_left, self.handleClientDisconnected
		)

	def registerCallbacks(self) -> None:
		patcher_callbacks = self._getPatcherCallbacks()
		for event, callback in patcher_callbacks:
			self.patcher.registerCallback(event, callback)
		self.patchCallbacksAdded = True

	def unregisterCallbacks(self):
		patcher_callbacks = self._getPatcherCallbacks()
		for event, callback in patcher_callbacks:
			self.patcher.unregisterCallback(event, callback)
		self.patchCallbacksAdded = False

	def handleVersionMismatch(self) -> None:
		# translators: Message for version mismatch
		message = _("""The version of the relay server which you have connected to is not compatible with this version of the Remote Client.
Please either use a different server or upgrade your version of the addon.""")
		ui.message(message)
		self.transport.close()

	def handleMOTD(self, motd: str, force_display=False):
		if force_display or self.shouldDisplayMotd(motd):
			gui.messageBox(
				parent=gui.mainFrame, caption=_("Message of the Day"), message=motd
			)

	def shouldDisplayMotd(self, motd: str) -> bool:
		conf = configuration.get_config()
		connection = self.getConnectionInfo()
		address = "{host}:{port}".format(host=connection.host, port=connection.port)
		motdBytes = motd.encode("utf-8", errors="surrogatepass")
		hashed = hashlib.sha1(motdBytes).hexdigest()
		current = conf["seen_motds"].get(address, "")
		if current == hashed:
			return False
		conf["seen_motds"][address] = hashed
		conf.write()
		return True

	def handleClientConnected(self, client: Optional[Dict[str, Any]] = None) -> None:
		self.patcher.register()
		if not self.patchCallbacksAdded:
			self.registerCallbacks()
		cues.client_connected()

	def handleClientDisconnected(self, client=None):
		cues.client_disconnected()

	def getConnectionInfo(self) -> connection_info.ConnectionInfo:
		hostname, port = self.transport.address
		key = self.transport.channel
		return connection_info.ConnectionInfo(
			hostname=hostname, port=port, key=key, mode=self.mode
		)


	def close(self) -> None:
		self.transport.close()
		
	def __del__(self) -> None:
		self.close()

class SlaveSession(RemoteSession):
	"""Session that runs on the slave and manages state."""

	mode: connection_info.ConnectionMode = connection_info.ConnectionMode.SLAVE
	patcher: nvda_patcher.NVDASlavePatcher
	masters: Dict[int, Dict[str, Any]]
	masterDisplaySizes: List[int]

	def __init__(
		self, localMachine: local_machine.LocalMachine, transport: RelayTransport
	) -> None:
		super().__init__(localMachine, transport)
		self.transport.registerInbound(RemoteMessageType.key, self.localMachine.sendKey)
		self.masters = defaultdict(dict)
		self.masterDisplaySizes = []
		self.transport.transportClosing.register(self.handleTransportClosing)
		self.patcher = nvda_patcher.NVDASlavePatcher()
		self.transport.registerInbound(
			RemoteMessageType.channel_joined, self.handleChannelJoined
		)
		self.transport.registerInbound(
			RemoteMessageType.set_braille_info, self.handleBrailleInfo
		)
		self.transport.registerInbound(
			RemoteMessageType.set_display_size, self.setDisplaySize
		)
		braille.filter_displaySize.register(self.localMachine.handleFilterDisplaySize)
		self.transport.registerInbound(
			RemoteMessageType.braille_input, self.localMachine.brailleInput
		)
		self.transport.registerInbound(
			RemoteMessageType.send_SAS, self.localMachine.sendSAS
		)

	def registerCallbacks(self) -> None:
		super().registerCallbacks()
		self.transport.registerOutbound(tones.decide_beep, RemoteMessageType.tone)
		self.transport.registerOutbound(speechCanceled, RemoteMessageType.cancel)
		self.transport.registerOutbound(
			nvwave.decide_playWaveFile, RemoteMessageType.wave
		)
		braille.pre_writeCells.register(self.display)

	def unregisterCallbacks(self) -> None:
		super().unregisterCallbacks()
		self.transport.unregisterOutbound(RemoteMessageType.tone)
		self.transport.unregisterOutbound(RemoteMessageType.cancel)
		self.transport.unregisterOutbound(RemoteMessageType.wave)

	def handleClientConnected(self, client: Dict[str, Any]) -> None:
		super().handleClientConnected(client)
		if client["connection_type"] == "master":
			self.masters[client["id"]]["active"] = True

	def handleChannelJoined(
		self,
		channel: Optional[str] = None,
		clients: Optional[List[Dict[str, Any]]] = None,
		origin: Optional[int] = None,
	) -> None:
		if clients is None:
			clients = []
		for client in clients:
			self.handleClientConnected(client)

	def handleTransportClosing(self) -> None:
		self.patcher.unregister()
		if self.patchCallbacksAdded:
			self.unregisterCallbacks()

	def handleTransportDisconnected(self):
		cues.client_connected()
		self.patcher.unregister()

	def handleClientDisconnected(self, client=None):
		super().handleClientDisconnected(client)
		if client["connection_type"] == "master":
			del self.masters[client["id"]]
		if not self.masters:
			self.patcher.unregister()

	def setDisplaySize(self, sizes=None):
		self.masterDisplaySizes = (
			sizes
			if sizes
			else [info.get("braille_numCells", 0) for info in self.masters.values()]
		)
		self.localMachine.setBrailleDisplay_size(self.masterDisplaySizes)

	def handleBrailleInfo(
		self,
		name: Optional[str] = None,
		numCells: int = 0,
		origin: Optional[int] = None,
	) -> None:
		if not self.masters.get(origin):
			return
		self.masters[origin]["braille_name"] = name
		self.masters[origin]["braille_numCells"] = numCells
		self.setDisplaySize()

	def _getPatcherCallbacks(self) -> List[Tuple[str, Callable[..., Any]]]:
		return (
			("speak", self.speak),
			("pause_speech", self.pauseSpeech),
			("set_display", self.setDisplaySize),
		)

	def _filterUnsupportedSpeechCommands(self, speechSequence: List[Any]) -> List[Any]:
		return list(
			[
				item
				for item in speechSequence
				if not isinstance(item, EXCLUDED_SPEECH_COMMANDS)
			]
		)

	def speak(self, speechSequence: List[Any], priority: Optional[str]) -> None:
		self.transport.send(
			RemoteMessageType.speak,
			sequence=self._filterUnsupportedSpeechCommands(speechSequence),
			priority=priority,
		)

	def pauseSpeech(self, switch):
		self.transport.send(type=RemoteMessageType.pause_speech, switch=switch)

	def display(self, cells: List[int]=None):
		# Only send braille data when there are controlling machines with a braille display
		if self.hasBrailleMasters():
			self.transport.send(type=RemoteMessageType.display, cells=cells)

	def hasBrailleMasters(self):
		return bool([i for i in self.masterDisplaySizes if i > 0])


class MasterSession(RemoteSession):
	mode: connection_info.ConnectionMode = connection_info.ConnectionMode.MASTER
	patcher: nvda_patcher.NVDAMasterPatcher
	slaves: Dict[int, Dict[str, Any]]

	def __init__(
		self, localMachine: local_machine.LocalMachine, transport: RelayTransport
	) -> None:
		super().__init__(localMachine, transport)
		self.slaves = defaultdict(dict)
		self.patcher = nvda_patcher.NVDAMasterPatcher()
		self.transport.registerInbound(RemoteMessageType.speak, self.localMachine.speak)
		self.transport.registerInbound(
			RemoteMessageType.cancel, self.localMachine.cancelSpeech
		)
		self.transport.registerInbound(
			RemoteMessageType.pause_speech, self.localMachine.pauseSpeech
		)
		self.transport.registerInbound(RemoteMessageType.tone, self.localMachine.beep)
		self.transport.registerInbound(
			RemoteMessageType.wave, self.localMachine.playWave
		)
		self.transport.registerInbound(
			RemoteMessageType.display, self.localMachine.display
		)
		self.transport.registerInbound(
			RemoteMessageType.nvda_not_connected, self.handleNVDANotConnected
		)
		self.transport.registerInbound(
			RemoteMessageType.channel_joined, self.handleChannel_joined
		)
		self.transport.registerInbound(
			RemoteMessageType.set_braille_info, self.sendBrailleInfo
		)

	def handleNVDANotConnected(self) -> None:
		speech.cancelSpeech()
		ui.message(_("Remote NVDA not connected."))

	def handleChannel_joined(
		self,
		channel: Optional[str] = None,
		clients: Optional[List[Dict[str, Any]]] = None,
		origin: Optional[int] = None,
	) -> None:
		if clients is None:
			clients = []
		for client in clients:
			self.handleClientConnected(client)

	def handleClientConnected(self, client=None):
		super().handleClientConnected(client)
		self.sendBrailleInfo()

	def handleClientDisconnected(self, client=None):
		super().handleClientDisconnected(client)
		self.patcher.unregister()
		if self.patchCallbacksAdded:
			self.unregisterCallbacks()

	def sendBrailleInfo(
		self, display: Optional[Any] = None, displaySize: Optional[int] = None
	) -> None:
		if display is None:
			display = braille.handler.display
		if displaySize is None:
			displaySize = braille.handler.displaySize
		self.transport.send(
			type="set_braille_info", name=display.name, numCells=displaySize
		)

	def brailleInput(self) -> None:
		self.transport.send(type=RemoteMessageType.braille_input)

	def _getPatcherCallbacks(self) -> List[Tuple[str, Callable[..., Any]]]:
		return (
			("braille_input", self.brailleInput),
			("set_display", self.sendBrailleInfo),
		)
