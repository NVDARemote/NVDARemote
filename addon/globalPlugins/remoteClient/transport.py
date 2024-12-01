"""Network transport layer for NVDA Remote.

This module provides the core networking functionality for NVDA Remote.

Classes:
    Transport: Base class defining the transport interface
    TCPTransport: Implementation of secure TCP socket transport  
    RelayTransport: Extended TCP transport for relay server connections
    ConnectorThread: Helper class for connection management

The transport layer handles:
    * Secure socket connections with SSL/TLS
    * Message serialization and deserialization 
    * Connection management and reconnection
    * Event notifications for connection state changes
"""

import hashlib
import select
import socket
import ssl
import threading
import time
from collections import defaultdict
from logging import getLogger
from queue import Queue
from typing import Any, Callable, Dict, Optional, Tuple, Union
from enum import Enum

from extensionPoints import Action
import wx

log = getLogger('transport')


from . import configuration
from .serializer import Serializer
from .socket_utils import SERVER_PORT, address_to_hostport, hostport_to_address
from .protocol import RemoteMessageType, PROTOCOL_VERSION
from .serializer import Serializer


class Transport:
	"""Base class defining the transport interface.
	
	This class provides the core interface for network transports,
	handling message routing and connection state.
	
	Attributes:
	    connected (bool): Whether transport is currently connected
	    successful_connects (int): Number of successful connections made
	    connected_event (threading.Event): Event set when connected
	    serializer (Serializer): Message serializer/deserializer
	    inboundHandlers (Dict[RemoteMessageType, Callable]): Message handlers
	
	Events:
	    transportConnected: Fired when connection is established
	    transportDisconnected: Fired when connection is lost
	    transportCertificateAuthenticationFailed: Fired on SSL cert verification failure
	    transportConnectionFailed: Fired when connection attempt fails
	    transportClosing: Fired when transport is being closed
	"""
	connected: bool
	successful_connects: int
	connected_event: threading.Event 
	serializer: Serializer



	def __init__(self, serializer: Serializer) -> None:
		self.serializer = serializer
		self.connected = False
		self.successful_connects = 0
		self.connectedEvent = threading.Event()
		# iterate over all the message types and create a dictionary of handlers mapping to Action()
		self.inboundHandlers: Dict[RemoteMessageType, Callable] = {msg: Action() for msg in RemoteMessageType}
		self.transportConnected = Action()
		"""
		Notifies when the transport is connected
		"""
		self.transportDisconnected = Action()
		"""
		Notifies when the transport is disconnected
		"""
		self.transportCertificateAuthenticationFailed = Action()
		"""
		Notifies when the transport fails to authenticate the certificate
		"""
		self.transportConnectionFailed = Action()
		"""
		Notifies when the transport fails to connect
		"""
		self.transportClosing = Action()
		"""
		Notifies when the transport is closing
		"""

	def onTransportConnected(self) -> None:
		self.successful_connects += 1
		self.connected = True
		self.connectedEvent.set()
		self.transportConnected.notify()

	def registerInbound(self, type: RemoteMessageType, handler: Callable) -> None:
		self.inboundHandlers[type].register(handler)

	def unregisterInbound(self, type: RemoteMessageType, handler: Callable) -> None:
		self.inboundHandlers[type].unregister(handler)

class TCPTransport(Transport):
	"""Secure TCP socket transport implementation.
	
	This class implements the Transport interface using TCP sockets with SSL/TLS
	encryption. It handles connection establishment, data transfer, and connection
	lifecycle management.
	
	Args:
	    serializer (Serializer): Message serializer instance
	    address (Tuple[str, int]): Remote address to connect to
	    timeout (int, optional): Connection timeout in seconds. Defaults to 0.
	    insecure (bool, optional): Skip certificate verification. Defaults to False.
	
	Attributes:
	    buffer (bytes): Buffer for incomplete received data
	    closed (bool): Whether transport is closed
	    queue (Queue[Optional[bytes]]): Queue of outbound messages
	    insecure (bool): Whether to skip certificate verification
	    address (Tuple[str, int]): Remote address to connect to
	    timeout (int): Connection timeout in seconds
	    server_sock (Optional[ssl.SSLSocket]): The SSL socket connection
	    server_sock_lock (threading.Lock): Lock for thread-safe socket access
	    queue_thread (Optional[threading.Thread]): Thread handling outbound messages
	    reconnector_thread (ConnectorThread): Thread managing reconnection
	"""
	buffer: bytes
	closed: bool
	queue: Queue[Optional[bytes]]
	insecure: bool
	server_sock_lock: threading.Lock
	address: Tuple[str, int]
	server_sock: Optional[ssl.SSLSocket]
	queue_thread: Optional[threading.Thread]
	timeout: int
	reconnector_thread: 'ConnectorThread'
	last_fail_fingerprint: Optional[str]
	
	def __init__(self, serializer: Serializer, address: Tuple[str, int], timeout: int = 0, insecure: bool = False) -> None:
		super().__init__(serializer=serializer)
		self.closed = False
		#Buffer to hold partially received data
		self.buffer = B''
		self.queue = Queue()
		self.address = address
		self.server_sock = None
		# Reading/writing from an SSL socket is not thread safe.
		# See https://bugs.python.org/issue41597#msg375692
		# Guard access to the socket with a lock.
		self.server_sock_lock = threading.Lock()
		self.queue_thread = None
		self.timeout = timeout
		self.reconnector_thread = ConnectorThread(self)
		self.insecure=insecure

	def run(self) -> None:
		self.closed = False
		try:
			self.server_sock = self.create_outbound_socket(*self.address, insecure=self.insecure)
			self.server_sock.connect(self.address)
		except ssl.SSLCertVerificationError as ex:
			fingerprint=None
			try:
				tmp_con = self.create_outbound_socket(*self.address, insecure = True)
				tmp_con.connect(self.address)
				certBin = tmp_con.getpeercert(True)
				tmp_con.close()
				fingerprint = hashlib.sha256(certBin).hexdigest().lower()
			except Exception: pass
			config = configuration.get_config()
			if hostport_to_address(self.address) in config['trusted_certs'] and config['trusted_certs'][hostport_to_address(self.address)]==fingerprint:
				self.insecure=True
				return self.run()
			self.last_fail_fingerprint = fingerprint
			self.transportCertificateAuthenticationFailed.notify()
			raise
		except Exception:
			self.transportConnectionFailed.notify()
			raise
		self.onTransportConnected()
		self.queue_thread = threading.Thread(target=self.send_queue)
		self.queue_thread.daemon = True
		self.queue_thread.start()
		while self.server_sock is not None:
			try:
				readers, writers, error = select.select([self.server_sock], [], [self.server_sock])
			except socket.error:
				self.buffer = b''
				break
			if self.server_sock in error:
				self.buffer = b""
				break
			if self.server_sock in readers:
				try:
					self.handle_server_data()
				except socket.error:
					self.buffer = b''
					break
		self.connected = False
		self.connectedEvent.clear()
		self.transportDisconnected.notify()
		self._disconnect()

	def create_outbound_socket(self, host: str, port: int, insecure: bool = False) -> ssl.SSLSocket:
		address = socket.getaddrinfo(host, port)[0]
		server_sock = socket.socket(*address[:3])
		if self.timeout:
			server_sock.settimeout(self.timeout)
		server_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		server_sock.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60000, 2000))
		ctx = (ssl.SSLContext())
		if insecure: ctx.verify_mode = ssl.CERT_NONE
		ctx.check_hostname = not insecure
		ctx.load_default_certs()
		server_sock = ctx.wrap_socket(sock=server_sock, server_hostname=host)
		return server_sock

	def getpeercert(self, binary_form: bool = False) -> Optional[Union[Dict[str, Any], bytes]]:
		if self.server_sock is None: return None
		return self.server_sock.getpeercert(binary_form)

	def handle_server_data(self) -> None:
		# This approach may be problematic:
		# See also server.py handle_data in class Client.
		buffSize = 16384
		with self.server_sock_lock:
			# select operates on the raw socket. Even though it said there was data to
			# read, that might be SSL data which might not result in actual data for
			# us. Therefore, do a non-blocking read so SSL doesn't try to wait for
			# more data for us.
			# We don't make the socket non-blocking earlier because then we'd have to
			# handle retries during the SSL handshake.
			# See https://stackoverflow.com/questions/3187565/select-and-ssl-in-python
			# and https://docs.python.org/3/library/ssl.html#notes-on-non-blocking-sockets
			self.server_sock.setblocking(False)
			try:
				data = self.buffer + self.server_sock.recv(buffSize)
			except ssl.SSLWantReadError:
				# There's no data for us.
				return
			finally:
				self.server_sock.setblocking(True)
		self.buffer = b''
		if not data:
			self._disconnect()
			return
		if b'\n' not in data:
			self.buffer += data
			return
		while b'\n' in data:
			line, sep, data = data.partition(b'\n')
			self.parse(line)
		self.buffer += data

	def parse(self, line: bytes) -> None:
		obj = self.serializer.deserialize(line)
		if 'type' not in obj:
			log.error("Received message without type: %r" % obj)
			return
		try:
			messageType = RemoteMessageType(obj['type'])
		except ValueError:
			log.error("Received message with invalid type: %r" % obj)
			return
		del obj['type']
		extensionPoint = self.inboundHandlers.get(messageType)
		if not extensionPoint:
			log.error("Received message with unhandled type: %r" % obj)
			return
		wx.CallAfter(extensionPoint.notify, **obj)

	def send_queue(self) -> None:
		while True:
			item = self.queue.get()
			if item is None:
				return
			try:
				with self.server_sock_lock:
					self.server_sock.sendall(item)
			except socket.error:
				return

	def send(self, type: str|Enum, **kwargs: Any) -> None:
		obj = self.serializer.serialize(type=type, **kwargs)
		if self.connected:
			self.queue.put(obj)

	def _disconnect(self):
		"""Disconnect the transport due to an error, without closing the connector thread."""
		if self.queue_thread is not None:
			self.queue.put(None)
			self.queue_thread.join()
			self.queue_thread = None
		clear_queue(self.queue)
		if self.server_sock:
			self.server_sock.close()
			self.server_sock = None

	def close(self):
		"""Close the transport."""
		self.transportClosing.notify()
		self.reconnector_thread.running = False
		self._disconnect()
		self.closed = True
		self.reconnector_thread = ConnectorThread(self)

class RelayTransport(TCPTransport):
	"""Transport for connecting through a relay server.
	
	Extends TCPTransport with relay-specific protocol handling for channels
	and connection types. Manages protocol versioning and channel joining.
	
	Args:
	    serializer (Any): Message serializer instance
	    address (Tuple[str, int]): Relay server address
	    timeout (int, optional): Connection timeout. Defaults to 0.
	    channel (Optional[str], optional): Channel to join. Defaults to None.
	    connection_type (Optional[str], optional): Connection type. Defaults to None.
	    protocol_version (int, optional): Protocol version. Defaults to PROTOCOL_VERSION.
	    insecure (bool, optional): Skip certificate verification. Defaults to False.
	
	Attributes:
	    channel (Optional[str]): Relay channel name
	    connection_type (Optional[str]): Type of relay connection
	    protocol_version (int): Protocol version to use
	"""
	channel: Optional[str]
	connection_type: Optional[str]
	protocol_version: int

	def __init__(
		self,
		serializer: Serializer,
		address: Tuple[str, int],
		timeout: int = 0,
		channel: Optional[str] = None,
		connection_type: Optional[str] = None,
		protocol_version: int = PROTOCOL_VERSION,
		insecure: bool = False
	) -> None:
		super().__init__(address=address, serializer=serializer, timeout=timeout, insecure=insecure)
		log.info("Connecting to %s channel %s" % (address, channel))
		self.channel = channel
		self.connection_type = connection_type
		self.protocol_version = protocol_version
		self.transportConnected.register(self.onConnected)



	def onConnected(self) -> None:
		self.send(RemoteMessageType.protocol_version, version=self.protocol_version)

		if self.channel is not None:
			self.send(RemoteMessageType.join, channel=self.channel, connection_type=self.connection_type)
		else:
			self.send(RemoteMessageType.generate_key)

class ConnectorThread(threading.Thread):
	"""Background thread that manages connection attempts.
	
	Handles automatic reconnection with configurable delay between attempts.
	Runs until explicitly stopped.
	
	Args:
	    connector (Transport): Transport instance to manage connections for
	    connect_delay (int, optional): Seconds between attempts. Defaults to 5.
	
	Attributes:
	    running (bool): Whether thread should continue running
	    connector (Transport): Transport to manage connections for
	    connect_delay (int): Seconds to wait between connection attempts
	"""
	running: bool
	connector: Transport
	connect_delay: int

	def __init__(self, connector: Transport, connect_delay: int = 5) -> None:
		super().__init__()
		self.connect_delay = connect_delay
		self.running = True
		self.connector = connector
		self.name = self.name + "_connector_loop"
		self.daemon = True

	def run(self):
		while self.running:
			try:
				self.connector.run()
			except socket.error:
				time.sleep(self.connect_delay)
				continue
			else:
				time.sleep(self.connect_delay)
		log.info("Ending control connector thread %s" % self.name)

def clear_queue(queue: Queue[Optional[bytes]]) -> None:
	"""Empty all items from a queue without blocking.
	
	Removes all items from the queue in a non-blocking way,
	useful for cleaning up before disconnection.
	
	Args:
	    queue (Queue[Optional[bytes]]): Queue instance to clear
	
	Note:
	    This function catches and ignores any exceptions that occur
	    while trying to get items from an empty queue.
	"""
	try:
		while True:
			queue.get_nowait()
	except Exception:
		pass
