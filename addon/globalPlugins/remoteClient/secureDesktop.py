import json
import socket
import ssl
import threading
import uuid
from dataclasses import dataclass
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


def get_program_data_temp_path() -> Path:
	"""Get the system's program data temp directory path."""
	if hasattr(shlobj, 'SHGetKnownFolderPath'):
		return Path(shlobj.SHGetKnownFolderPath(shlobj.FolderId.PROGRAM_DATA)) / 'temp'
	return Path(shlobj.SHGetFolderPath(0, shlobj.CSIDL_COMMON_APPDATA)) / 'temp'

@dataclass(frozen=True)
class SecureDesktopConnection:
	"""Connection details for secure desktop."""
	address: Tuple[str, int]
	channel: str

class SecureDesktopHandler:
	"""Handles secure desktop transitions and management of secure desktop connections."""
	
	SD_CONNECT_BLOCK_TIMEOUT: int = 1

	def __init__(self, temp_path: Path = get_program_data_temp_path()) -> None:
		"""
		Initialize secure desktop handler.
		
		Args:
			temp_path: Path to temporary directory for IPC file. Defaults to program data temp path.
		"""
		self.temp_path = temp_path
		self.ipc_file = temp_path / 'remote.ipc'
		
		self._slave_session: Optional[SlaveSession] = None
		self.sd_server: Optional[server.LocalRelayServer] = None
		self.sd_relay: Optional[RelayTransport] = None
		self.sd_bridge: Optional[bridge.BridgeTransport] = None

		post_secureDesktopStateChange.register(self._on_secure_desktop_change)

	def terminate(self) -> None:
		"""Clean up handler resources."""
		post_secureDesktopStateChange.unregister(self._on_secure_desktop_change)
		self.leave_secure_desktop()
		try:
			self.ipc_file.unlink()
		except FileNotFoundError:
			pass

	@property
	def slave_session(self) -> Optional[SlaveSession]:
		return self._slave_session

	@slave_session.setter
	def slave_session(self, session: Optional[SlaveSession]) -> None:
		"""
		Update slave session reference and handle necessary cleanup/setup.
		
		Args:
			session: New SlaveSession instance or None to clear
		"""
		if self._slave_session == session:
			return
			
		if self.sd_server is not None:
			self.leave_secure_desktop()
			
		if self._slave_session is not None and self._slave_session.transport is not None:
			transport = self._slave_session.transport
			transport.unregisterInbound(RemoteMessageType.set_braille_info, self._on_master_display_change)
		self._slave_session = session

	def _on_secure_desktop_change(self, isSecureDesktop: Optional[bool] = None) -> None:
		"""
		Internal callback for secure desktop state changes.
		
		Args:
			isSecureDesktop: True if transitioning to secure desktop, False otherwise
		"""
		if isSecureDesktop:
			self.enter_secure_desktop()
		else:
			self.leave_secure_desktop()

	def enter_secure_desktop(self) -> None:
		"""Set up necessary components when entering secure desktop."""
		if self.slave_session is None or self.slave_session.transport is None:
			log.warning("No slave session connected, not entering secure desktop.")
			return
		if not self.temp_path.exists():
			self.temp_path.mkdir(parents=True, exist_ok=True)

		channel = str(uuid.uuid4())
		self.sd_server = server.LocalRelayServer(port=0, password=channel, bind_host='127.0.0.1')
		port = self.sd_server.serverSocket.getsockname()[1]
		
		server_thread = threading.Thread(target=self.sd_server.run)
		server_thread.daemon = True
		server_thread.start()

		self.sd_relay = RelayTransport(
			address=('127.0.0.1', port),
			serializer=JSONSerializer(),
			channel=channel,
			insecure=True
		)
		self.sd_relay.registerInbound(RemoteMessageType.client_joined, self._on_master_display_change)
		self.slave_session.transport.registerInbound(RemoteMessageType.set_braille_info, self._on_master_display_change)
		
		self.sd_bridge = bridge.BridgeTransport(self.slave_session.transport, self.sd_relay)
		
		relay_thread = threading.Thread(target=self.sd_relay.run)
		relay_thread.daemon = True
		relay_thread.start()

		data = [port, channel]
		self.ipc_file.write_text(json.dumps(data))

	def leave_secure_desktop(self) -> None:
		"""Clean up when leaving secure desktop."""
		if self.sd_server is None:
			return

		if self.sd_bridge is not None:
			self.sd_bridge.disconnect()
			self.sd_bridge = None
		
		if self.sd_server is not None:
			self.sd_server.close()
			self.sd_server = None
		
		if self.sd_relay is not None:
			self.sd_relay.close()
			self.sd_relay = None

		if self.slave_session is not None and self.slave_session.transport is not None:
			self.slave_session.transport.unregisterInbound(RemoteMessageType.set_braille_info, self._on_master_display_change)
			self.slave_session.setDisplaySize()
		
		try:
			self.ipc_file.unlink()
		except FileNotFoundError:
			pass

	def initialize_secure_desktop(self) -> Optional[SecureDesktopConnection]:
		"""
		Initialize connection when starting in secure desktop.
		
		Returns:
			SecureDesktopConnection if successful, None if not
		"""
		try:
			data = json.loads(self.ipc_file.read_text())
			self.ipc_file.unlink()
			port, channel = data

			test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			test_socket = ssl.wrap_socket(test_socket)
			test_socket.connect(('127.0.0.1', port))
			test_socket.close()

			return SecureDesktopConnection(
				address=('127.0.0.1', port),
				channel=channel
			)
			
		except Exception:
			log.exception("Failed to initialize secure desktop connection.")
			return None

	def _on_master_display_change(self, **kwargs: Any) -> None:
		"""Handle display size changes."""
		if self.sd_relay is not None and self.slave_session is not None:
			self.sd_relay.send(
				type=RemoteMessageType.set_display_size,
				sizes=self.slave_session.masterDisplaySizes
			)
