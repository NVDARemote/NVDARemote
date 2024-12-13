"""Secure desktop support for NVDA Remote.

This module handles the transition between regular and secure desktop sessions in Windows,
maintaining remote connections across these transitions. It manages the creation of local
relay servers, connection bridging, and IPC (Inter-Process Communication) between the 
regular and secure desktop instances of NVDA.

The secure desktop is a special Windows session used for UAC prompts and login screens
that runs in an isolated environment for security. This module ensures NVDA Remote
connections persist when entering and leaving this secure environment.
"""

from dataclasses import dataclass
import json
import socket
import ssl
import threading
import uuid
from pathlib import Path
from typing import Any, Optional, Tuple

import shlobj
from logHandler import log
from winAPI.secureDesktop import post_secureDesktopStateChange

from . import bridge, server
from .protocol import RemoteMessageType
from .serializer import JSONSerializer
from .session import SlaveSession
from .transport import RelayTransport


def getProgramDataTempPath() -> Path:
	"""Get the system's program data temp directory path."""
	if hasattr(shlobj, 'SHGetKnownFolderPath'):
		return Path(shlobj.SHGetKnownFolderPath(shlobj.FolderId.PROGRAM_DATA)) / 'temp'
	return Path(shlobj.SHGetFolderPath(0, shlobj.CSIDL_COMMON_APPDATA)) / 'temp'


@dataclass(frozen=True)
class SecureDesktopConnection:
	"""Immutable container for secure desktop connection details.
	
	This class stores the connection information needed to establish
	a connection to a secure desktop session. The frozen=True decorator
	ensures instances are immutable after creation.
	
	Attributes:
		address (Tuple[str, int]): The (host, port) tuple for the connection
		channel (str): Unique channel identifier/password for the secure connection
	"""
	address: Tuple[str, int]
	channel: str


class SecureDesktopHandler:
	"""Manages transitions between regular and secure desktop environments.
	
	This class coordinates the complex process of maintaining NVDA Remote
	connections when Windows switches between regular and secure desktop
	sessions. It handles:
	
	* Setting up local relay servers for secure desktop communication
	* Managing IPC between regular and secure desktop NVDA instances
	* Bridging connections between the secure desktop and remote partner
	* Cleaning up resources when transitioning between desktop states
	
	The handler uses a temporary file for IPC and creates local relay servers
	to maintain connection state across desktop transitions.
	"""
	
	SD_CONNECT_BLOCK_TIMEOUT: int = 1

	def __init__(self, temp_path: Path = getProgramDataTempPath()) -> None:
		"""
		Initialize secure desktop handler.
		
		Args:
			temp_path: Path to temporary directory for IPC file. Defaults to program data temp path.
		"""
		self.tempPath = temp_path
		self.IPCFile = temp_path / 'remote.ipc'
		
		self._slaveSession: Optional[SlaveSession] = None
		self.sdServer: Optional[server.LocalRelayServer] = None
		self.sdRelay: Optional[RelayTransport] = None
		self.sdBridge: Optional[bridge.BridgeTransport] = None

		post_secureDesktopStateChange.register(self._onSecureDesktopChange)

	def terminate(self) -> None:
		"""Clean up handler resources."""
		post_secureDesktopStateChange.unregister(self._onSecureDesktopChange)
		self.leaveSecureDesktop()
		try:
			self.IPCFile.unlink()
		except FileNotFoundError:
			pass

	@property
	def slaveSession(self) -> Optional[SlaveSession]:
		return self._slaveSession

	@slaveSession.setter
	def slaveSession(self, session: Optional[SlaveSession]) -> None:
		"""
		Update slave session reference and handle necessary cleanup/setup.
		
		Args:
			session: New SlaveSession instance or None to clear
		"""
		if self._slaveSession == session:
			return
			
		if self.sdServer is not None:
			self.leaveSecureDesktop()
			
		if self._slaveSession is not None and self._slaveSession.transport is not None:
			transport = self._slaveSession.transport
			transport.unregisterInbound(RemoteMessageType.set_braille_info, self._onMasterDisplayChange)
		self._slaveSession = session

	def _onSecureDesktopChange(self, isSecureDesktop: Optional[bool] = None) -> None:
		"""
		Internal callback for secure desktop state changes.
		
		Args:
			isSecureDesktop: True if transitioning to secure desktop, False otherwise
		"""
		if isSecureDesktop:
			self.enterSecureDesktop()
		else:
			self.leaveSecureDesktop()

	def enterSecureDesktop(self) -> None:
		"""Set up necessary components when entering secure desktop."""
		if self.slaveSession is None or self.slaveSession.transport is None:
			log.warning("No slave session connected, not entering secure desktop.")
			return
		if not self.tempPath.exists():
			self.tempPath.mkdir(parents=True, exist_ok=True)

		channel = str(uuid.uuid4())
		self.sdServer = server.LocalRelayServer(port=0, password=channel, bind_host='127.0.0.1')
		port = self.sdServer.serverSocket.getsockname()[1]
		
		serverThread = threading.Thread(target=self.sdServer.run)
		serverThread.daemon = True
		serverThread.start()

		self.sdRelay = RelayTransport(
			address=('127.0.0.1', port),
			serializer=JSONSerializer(),
			channel=channel,
			insecure=True
		)
		self.sdRelay.registerInbound(RemoteMessageType.client_joined, self._onMasterDisplayChange)
		self.slaveSession.transport.registerInbound(RemoteMessageType.set_braille_info, self._onMasterDisplayChange)
		
		self.sdBridge = bridge.BridgeTransport(self.slaveSession.transport, self.sdRelay)
		
		relayThread = threading.Thread(target=self.sdRelay.run)
		relayThread.daemon = True
		relayThread.start()

		data = [port, channel]
		self.IPCFile.write_text(json.dumps(data))

	def leaveSecureDesktop(self) -> None:
		"""Clean up when leaving secure desktop."""
		if self.sdServer is None:
			return

		if self.sdBridge is not None:
			self.sdBridge.disconnect()
			self.sdBridge = None
		
		if self.sdServer is not None:
			self.sdServer.close()
			self.sdServer = None
		
		if self.sdRelay is not None:
			self.sdRelay.close()
			self.sdRelay = None

		if self.slaveSession is not None and self.slaveSession.transport is not None:
			self.slaveSession.transport.unregisterInbound(RemoteMessageType.set_braille_info, self._onMasterDisplayChange)
			self.slaveSession.setDisplaySize()
		
		try:
			self.IPCFile.unlink()
		except FileNotFoundError:
			pass

	def initializeSecureDesktop(self) -> Optional[SecureDesktopConnection]:
		"""
		Initialize connection when starting in secure desktop.
		
		Returns:
			SecureDesktopConnection if successful, None if not
		"""
		try:
			data = json.loads(self.IPCFile.read_text())
			self.IPCFile.unlink()
			port, channel = data

			testSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			testSocket = ssl.wrap_socket(testSocket)
			testSocket.connect(('127.0.0.1', port))
			testSocket.close()

			return SecureDesktopConnection(
				address=('127.0.0.1', port),
				channel=channel
			)
			
		except Exception:
			log.exception("Failed to initialize secure desktop connection.")
			return None

	def _onMasterDisplayChange(self, **kwargs: Any) -> None:
		"""Handle display size changes."""
		if self.sdRelay is not None and self.slaveSession is not None:
			self.sdRelay.send(
				type=RemoteMessageType.set_display_size,
				sizes=self.slaveSession.masterDisplaySizes
			)
