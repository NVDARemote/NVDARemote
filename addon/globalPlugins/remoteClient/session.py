"""Session management for NVDA Remote connections.

This module implements the core session management functionality for NVDA Remote,
handling both master and slave connections. It provides classes that manage the
state and behavior of remote NVDA instances connected through a relay server.

Key Components:
--------------
MasterSession
    Runs on the controlling NVDA instance. Sends commands and receives feedback.
    Handles keyboard input, braille routing, and display synchronization.

SlaveSession
    Runs on the controlled NVDA instance. Executes received commands and forwards
    speech/braille output back to master(s).

Architecture:
------------
The session layer sits between:
- Transport layer (below): Handles encrypted network communication
- Local Machine layer (above): Interfaces with the local NVDA instance

Core Responsibilities:
--------------------
1. Connection Management:
   - Version compatibility checking
   - Connection state tracking
   - Multiple client support
   - Message of the day handling

2. Feature Synchronization:
   - Speech output routing
   - Braille display coordination
   - Input command processing
   - System audio forwarding

3. Security:
   - Connection validation
   - Safe NVDA feature patching
   - Secure message routing

Example Usage:
-------------
Master instance:
    >>> transport = RelayTransport(address=("nvdaremote.com", 6837))
    >>> local = LocalMachine()
    >>> session = MasterSession(local_machine=local, transport=transport)
    >>> session.transport.connect()

Slave instance:
    >>> transport = RelayTransport(address=("nvdaremote.com", 6837))
    >>> local = LocalMachine()
    >>> session = SlaveSession(local_machine=local, transport=transport)
    >>> session.transport.connect()

See Also:
    - transport.py: For network communication implementation
    - local_machine.py: For NVDA interface implementation
    - nvda_patcher.py: For NVDA feature modification details
"""

import hashlib
from collections import defaultdict
from typing import Dict, List, Optional, Tuple, Union, Any, Callable
from dataclasses import dataclass


import addonHandler
import braille
import gui
import speech
import ui
import versionInfo
from logHandler import log

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
	"""Base class for a session that runs on either the master or slave machine.
	
	This abstract base class defines the core functionality shared between master and slave
	sessions. It handles basic session management tasks like:
	
	- Version compatibility checking
	- Message of the day handling 
	- Connection info management
	- Transport registration
	
	Args:
		local_machine (LocalMachine): Interface to local NVDA instance
		transport (RelayTransport): Network transport layer instance
	
	Attributes:
		transport (RelayTransport): The transport layer handling network communication
		localMachine (LocalMachine): Interface to control the local NVDA instance
		mode (Optional[str]): Session mode - either 'master' or 'slave'
		patcher (Optional[NVDAPatcher]): Patcher instance for NVDA modifications
	"""

	transport: RelayTransport
	localMachine: local_machine.LocalMachine
	mode: Optional[str] = None
	patcher: Optional[nvda_patcher.NVDAPatcher]

	def __init__(self, localMachine: local_machine.LocalMachine, transport: RelayTransport) -> None:
		self.localMachine = localMachine
		self.patcher = None
		self.transport = transport
		self.transport.registerInbound(RemoteMessageType.version_mismatch, self.handleVersionMismatch)
		self.transport.registerInbound(RemoteMessageType.motd, self.handleMotd)


	def handleVersionMismatch(self) -> None:
		"""Handle protocol version mismatch between client and server.

		This method is called when the relay server detects that the client's
		protocol version is not compatible. It:
		1. Displays a localized error message to the user
		2. Closes the transport connection
		3. Prevents further communication attempts

		Note:
			Version compatibility is checked during initial handshake.
			The connection is immediately terminated if versions mismatch.
		"""
		# translators: Message for version mismatch
		message = _("""The version of the relay server which you have connected to is not compatible with this version of the Remote Client.
Please either use a different server or upgrade your version of the addon.""")
		ui.message(message)
		self.transport.close()

	def handleMotd(self, motd: str, force_display: bool = False) -> None:
		"""Handle Message of the Day from relay server.

		Displays server MOTD to user if:
		1. It hasn't been shown before (tracked by SHA1 hash), or
		2. force_display is True (for important announcements)

		The MOTD system allows server operators to communicate important
		information to users like:
		- Service announcements
		- Maintenance windows
		- Version update notifications
		- Security advisories

		Args:
			motd: The message text to display
			force_display: If True, always show message regardless of previous views

		Note:
			MOTD hashes are stored per-server in the config file to track
			which messages have already been shown to the user.
		"""
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
	"""Session that runs on the controlled (slave) NVDA instance.
	
	This class implements the slave side of an NVDA Remote connection. It handles:
	
	- Receiving and executing commands from master(s)
	- Forwarding speech/braille/audio output to master(s)
	- Managing connected master clients
	- Coordinating braille display sizes
	- Patching NVDA functionality for remote control
	
	The slave session allows multiple master connections simultaneously and manages
	state for each connected master separately.
	
	Attributes:
		mode (str): Always 'slave' for this class
		masters (Dict[int, Dict[str, Any]]): Information about connected master clients
		masterDisplaySizes (List[int]): Braille display sizes of connected masters
		patchCallbacksAdded (bool): Whether callbacks are currently registered
		patcher (NVDASlavePatcher): Patcher for slave-specific NVDA modifications
	"""

	mode: connection_info.ConnectionMode = connection_info.ConnectionMode.SLAVE
	patcher: nvda_patcher.NVDASlavePatcher
	masters: Dict[int, Dict[str, Any]]
	masterDisplaySizes: List[int]
	patchCallbacksAdded: bool

	def __init__(self, localMachine: local_machine.LocalMachine, transport: RelayTransport) -> None:
		super().__init__(localMachine, transport)
		self.transport.registerInbound(RemoteMessageType.client_joined, self.handleClientConnected)
		self.transport.registerInbound(RemoteMessageType.client_left, self.handleClientDisconnected)
		self.transport.registerInbound(RemoteMessageType.key, self.localMachine.sendKey)
		self.masters = defaultdict(dict)
		self.masterDisplaySizes = []
		self.transport.registerInbound(RemoteMessageType.index, self.recvIndex)
		self.transport.transportClosing.register(self.handleTransportClosing)
		self.patcher = nvda_patcher.NVDASlavePatcher()
		self.patchCallbacksAdded = False
		self.transport.registerInbound(RemoteMessageType.channel_joined, self.handleChannelJoined)
		self.transport.registerInbound(RemoteMessageType.set_clipboard_text, self.localMachine.setClipboardText)
		self.transport.registerInbound(RemoteMessageType.set_braille_info, self.handleBrailleInfo)
		self.transport.registerInbound(RemoteMessageType.set_display_size, self.setDisplaySize)
		braille.filter_displaySize.register(
			self.localMachine.handleFilterDisplaySize)
		self.transport.registerInbound(RemoteMessageType.braille_input, self.localMachine.brailleInput)
		self.transport.registerInbound(RemoteMessageType.send_SAS, self.localMachine.sendSAS)

	def handleClientConnected(self, client: Optional[Dict[str, Any]] = None) -> None:
		self.patcher.patch()
		if not self.patchCallbacksAdded:
			self.addPatchCallbacks()
			self.patchCallbacksAdded = True
		cues.client_connected()
		if client['connection_type'] == 'master':
			self.masters[client['id']]['active'] = True

	def handleChannelJoined(self, channel: Optional[str] = None, clients: Optional[List[Dict[str, Any]]] = None, origin: Optional[int] = None) -> None:
		if clients is None:
			clients = []
		for client in clients:
			self.handleClientConnected(client)

	def handleTransportClosing(self) -> None:
		self.patcher.unpatch()
		if self.patchCallbacksAdded:
			self.removePatchCallbacks()
			self.patchCallbacksAdded = False

	def handleTransportDisconnected(self):
		cues.client_connected()
		self.patcher.unpatch()

	def handleClientDisconnected(self, client=None):
		cues.client_disconnected()
		if client['connection_type'] == 'master':
			del self.masters[client['id']]
		if not self.masters:
			self.patcher.unpatch()

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

	def _getPatcherCallbacks(self) -> List[Tuple[str, Callable[..., Any]]]:
		return (
			('speak', self.speak),
				('beep', self.beep),
				('wave', self.playWaveFile),
				('cancel_speech', self.cancelSpeech),
				('pause_speech', self.pauseSpeech),
				('display', self.display),
				('set_display', self.setDisplaySize)
		)

	def addPatchCallbacks(self) -> None:
		patcher_callbacks = self._getPatcherCallbacks()
		for event, callback in patcher_callbacks:
			self.patcher.registerCallback(event, callback)

	def removePatchCallbacks(self):
		patcher_callbacks = self._getPatcherCallbacks()
		for event, callback in patcher_callbacks:
			self.patcher.unregisterCallback(event, callback)

	def _filterUnsupportedSpeechCommands(self, speechSequence: List[Any]) -> List[Any]:
		return list([
			item for item in speechSequence
			if not isinstance(item, EXCLUDED_SPEECH_COMMANDS)
		])

	def speak(self, speechSequence: List[Any], priority: Optional[str]) -> None:
		self.transport.send(RemoteMessageType.speak,
							sequence=self._filterUnsupportedSpeechCommands(
								speechSequence),
							priority=priority
							)

	def cancelSpeech(self):
		self.transport.send(type=RemoteMessageType.cancel)

	def pauseSpeech(self, switch):
		self.transport.send(type=RemoteMessageType.pause_speech, switch=switch)

	def beep(self, hz: float, length: int, left: int = 50, right: int = 50) -> None:
		self.transport.send(type=RemoteMessageType.tone, hz=hz,
		                    length=length, left=left, right=right)

	def playWaveFile(self, **kwargs):
		"""This machine played a sound, send it to Master machine"""
		kwargs.update({
			# nvWave.playWaveFile should always be asynchronous when called from NVDA remote, so always send 'True'
				# Version 2.2 requires 'async' keyword.
				'async': True,
				# Version 2.3 onwards. Not currently used, but matches arguments for nvWave.playWaveFile.
				# Including it allows for forward compatibility if requirements change.
				'asynchronous': True,
		})
		self.transport.send(type=RemoteMessageType.wave)

	def display(self, cells):
		# Only send braille data when there are controlling machines with a braille display
		if self.hasBrailleMasters():
			self.transport.send(type=RemoteMessageType.display, cells=cells)

	def hasBrailleMasters(self):
		return bool([i for i in self.masterDisplaySizes if i > 0])

	def recvIndex(self, index=None):
		pass  # speech index approach changed in 2019.3


class MasterSession(RemoteSession):
	"""Session that runs on the controlling (master) NVDA instance.
	
	This class implements the master side of an NVDA Remote connection. It handles:
	
	- Sending control commands to slaves
	- Receiving and playing speech/braille/audio from slaves
	- Managing connected slave clients
	- Synchronizing braille display information
	- Patching NVDA for remote input handling
	
	The master session takes input from the local NVDA instance and forwards
	appropriate commands to control the remote slave instance.
	
	Attributes:
		mode (str): Always 'master' for this class
		slaves (Dict[int, Dict[str, Any]]): Information about connected slave clients
		patchCallbacksAdded (bool): Whether callbacks are currently registered
		patcher (NVDAMasterPatcher): Patcher for master-specific NVDA modifications
	"""

	mode: connection_info.ConnectionMode = connection_info.ConnectionMode.MASTER
	patcher: nvda_patcher.NVDAMasterPatcher
	slaves: Dict[int, Dict[str, Any]]
	patchCallbacksAdded: bool

	def __init__(self, localMachine: local_machine.LocalMachine, transport: RelayTransport) -> None:
		super().__init__(localMachine, transport)
		self.slaves = defaultdict(dict)
		self.patcher = nvda_patcher.NVDAMasterPatcher()
		self.patchCallbacksAdded = False
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
		self.patcher.patch()
		if not self.patchCallbacksAdded:
			self.addPatchCallbacks()
			self.patchCallbacksAdded = True
		self.sendBrailleInfo()
		cues.client_connected()

	def handleClientDisconnected(self, client=None):
		self.patcher.unpatch()
		if self.patchCallbacksAdded:
			self.removePatchCallbacks()
			self.patchCallbacksAdded = False
		cues.client_disconnected()

	def sendBrailleInfo(self, display: Optional[Any] = None, displaySize: Optional[int] = None) -> None:
		if display is None:
			display = braille.handler.display
		if displaySize is None:
			displaySize = braille.handler.displaySize
		self.transport.send(type="set_braille_info",
							name=display.name, numCells=displaySize)

	def brailleInput(self) -> None:
		self.transport.send(type=RemoteMessageType.braille_input)

	def addPatchCallbacks(self):
		patcher_callbacks = (('braille_input', self.brailleInput),
							 ('set_display', self.sendBrailleInfo))
		for event, callback in patcher_callbacks:
			self.patcher.registerCallback(event, callback)

	def removePatchCallbacks(self):
		patcher_callbacks = (('braille_input', self.brailleInput),
							 ('set_display', self.sendBrailleInfo))
		for event, callback in patcher_callbacks:
			self.patcher.unregisterCallback(event, callback)
