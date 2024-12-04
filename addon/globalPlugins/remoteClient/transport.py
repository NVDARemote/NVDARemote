"""Network transport layer for NVDA Remote.

Provides secure network communication between NVDA instances using SSL/TLS.
Handles connection management, message serialization, and event notifications.

Key features:
    * SSL/TLS encrypted connections
    * Automatic reconnection
    * Message type-based routing
    * Background socket operations
    * Main thread message handling for UI safety
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
from .socket_utils import addressToHostPort, hostPortToAddress
from .protocol import SERVER_PORT, RemoteMessageType, PROTOCOL_VERSION
from .serializer import Serializer


class Transport:
	"""Base class for network transport implementations.
	
	Subclass this to implement a new transport type. Key requirements:
	1. Implement run() for connection logic
	2. Call onTransportConnected() when connected
	3. Use send() for outbound messages
	4. Fire appropriate events for connection state changes
	
	Args:
	    serializer: Message serializer for encoding/decoding
	
	Attributes:
	    connected (bool): Connection state
	    successfulConnects (int): Connection attempt counter
	    connectedEvent (threading.Event): Set when connected
	    serializer (Serializer): Message serializer
	    inboundHandlers (Dict[RemoteMessageType, Callable]): Message handlers
	
	Events:
	    transportConnected: Connection established
	    transportDisconnected: Connection lost
	    transportCertificateAuthenticationFailed: SSL validation failed  
	    transportConnectionFailed: Connection attempt failed
	    transportClosing: Transport shutting down
	"""
	connected: bool
	successfulConnects: int
	connectedEvent: threading.Event 
	serializer: Serializer


	def __init__(self, serializer: Serializer) -> None:
		self.serializer = serializer
		self.connected = False
		self.successfulConnects = 0
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
		"""Update state and notify listeners on successful connection."""
		self.successful_connects += 1
		self.connected = True
		self.connectedEvent.set()
		self.transportConnected.notify()

	def registerInbound(self, type: RemoteMessageType, handler: Callable) -> None:
		"""Register a message handler.

		Args:
			type (RemoteMessageType): Message type to handle
			handler (Callable): Handler function called with message kwargs
			
		Note: Handlers run on wx main thread via CallAfter
		"""
		self.inboundHandlers[type].register(handler)

	def unregisterInbound(self, type: RemoteMessageType, handler: Callable) -> None:
		"""Remove a message handler.

		Args:
			type (RemoteMessageType): Message type to unregister from
			handler (Callable): Handler function to remove
		"""
		self.inboundHandlers[type].unregister(handler)

class TCPTransport(Transport):
	"""SSL/TLS encrypted TCP transport.
	
	Args:
	    serializer (Serializer): Message serializer
	    address (Tuple[str, int]): Remote address
	    timeout (int, optional): Connection timeout seconds. Default 0
	    insecure (bool, optional): Skip cert verification. Default False
	
	Attributes:
	    buffer (bytes): Incomplete received data
	    closed (bool): Transport closed state
	    queue (Queue[Optional[bytes]]): Outbound messages
	    insecure (bool): Skip cert verification
	    address (Tuple[str, int]): Remote address
	    timeout (int): Connection timeout
	    serverSock (Optional[ssl.SSLSocket]): SSL socket
	    serverSockLock (threading.Lock): Socket access lock
	    queue_thread (Optional[threading.Thread]): Outbound message thread
	    reconnector_thread (ConnectorThread): Reconnection manager
	    lastFailFingerprint (Optional[str]): Last failed cert fingerprint
	"""
	buffer: bytes
	closed: bool
	queue: Queue[Optional[bytes]]
	insecure: bool
	serverSockLock: threading.Lock
	address: Tuple[str, int]
	serverSock: Optional[ssl.SSLSocket]
	queue_thread: Optional[threading.Thread]
	timeout: int
	reconnector_thread: 'ConnectorThread'
	lastFailFingerprint: Optional[str]
	
	def __init__(self, serializer: Serializer, address: Tuple[str, int], timeout: int = 0, insecure: bool = False) -> None:
		super().__init__(serializer=serializer)
		self.closed = False
		#Buffer to hold partially received data
		self.buffer = B''
		self.queue = Queue()
		self.address = address
		self.serverSock = None
		# Reading/writing from an SSL socket is not thread safe.
		# See https://bugs.python.org/issue41597#msg375692
		# Guard access to the socket with a lock.
		self.serverSockLock = threading.Lock()
		self.queue_thread = None
		self.timeout = timeout
		self.reconnector_thread = ConnectorThread(self)
		self.insecure=insecure

	def run(self) -> None:
		self.closed = False
		try:
			self.serverSock = self.create_outbound_socket(*self.address, insecure=self.insecure)
			self.serverSock.connect(self.address)
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
			if hostPortToAddress(self.address) in config['trusted_certs'] and config['trusted_certs'][hostPortToAddress(self.address)]==fingerprint:
				self.insecure=True
				return self.run()
			self.lastFailFingerprint = fingerprint
			self.transportCertificateAuthenticationFailed.notify()
			raise
		except Exception:
			self.transportConnectionFailed.notify()
			raise
		self.onTransportConnected()
		self.queue_thread = threading.Thread(target=self.send_queue)
		self.queue_thread.daemon = True
		self.queue_thread.start()
		while self.serverSock is not None:
			try:
				readers, writers, error = select.select([self.serverSock], [], [self.serverSock])
			except socket.error:
				self.buffer = b''
				break
			if self.serverSock in error:
				self.buffer = b""
				break
			if self.serverSock in readers:
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
		"""Create and configure an SSL socket for outbound connections.

		Creates a TCP socket with appropriate timeout and keep-alive settings,
		then wraps it with SSL/TLS encryption.

		Args:
			host (str): Remote hostname to connect to
			port (int): Remote port number
			insecure (bool, optional): Skip certificate verification. Defaults to False.

		Returns:
			ssl.SSLSocket: Configured SSL socket ready for connection

		Note:
			The socket is created but not yet connected. Call connect() separately.
		"""
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
		"""Get peer's SSL certificate.

		Args:
			binary_form (bool): Return raw bytes if True, dict if False

		Returns:
			Optional[Union[Dict[str, Any], bytes]]: Certificate or None
		"""
		if self.serverSock is None: return None
		return self.serverSock.getpeercert(binary_form)

	def handle_server_data(self) -> None:
		"""Process incoming data from the server socket.

		Reads available data from the socket, buffers partial messages,
		and processes complete messages by passing them to parse().

		Messages are expected to be newline-delimited.
		Partial messages are stored in self.buffer until complete.

		Note:
			This method handles SSL-specific socket behavior and non-blocking reads.
			It is called when select() indicates data is available.
		"""
		# This approach may be problematic:
		# See also server.py handle_data in class Client.
		buffSize = 16384
		with self.serverSockLock:
			# select operates on the raw socket. Even though it said there was data to
			# read, that might be SSL data which might not result in actual data for
			# us. Therefore, do a non-blocking read so SSL doesn't try to wait for
			# more data for us.
			# We don't make the socket non-blocking earlier because then we'd have to
			# handle retries during the SSL handshake.
			# See https://stackoverflow.com/questions/3187565/select-and-ssl-in-python
			# and https://docs.python.org/3/library/ssl.html#notes-on-non-blocking-sockets
			self.serverSock.setblocking(False)
			try:
				data = self.buffer + self.serverSock.recv(buffSize)
			except ssl.SSLWantReadError:
				# There's no data for us.
				return
			finally:
				self.serverSock.setblocking(True)
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
		"""Parse and handle a complete message line.

		Deserializes a message and routes it to the appropriate handler based on type.

		Args:
			line (bytes): Complete message line to parse

		Note:
			Messages must include a 'type' field matching a RemoteMessageType enum value.
			Handler callbacks are executed asynchronously on the wx main thread.
			Invalid or unhandled message types are logged as errors.
		"""
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
		"""Background thread that processes the outbound message queue.

		Continuously pulls messages from the queue and sends them over the socket.
		Thread exits when None is received from the queue or a socket error occurs.

		Note:
			This method runs in a separate thread and handles thread-safe socket access
			using the server_sock_lock.
		"""
		while True:
			item = self.queue.get()
			if item is None:
				return
			try:
				with self.serverSockLock:
					self.serverSock.sendall(item)
			except socket.error:
				return

	def send(self, type: str|Enum, **kwargs: Any) -> None:
		"""Send a message through the transport.

		Serializes and queues a message for transmission. Messages are sent
		asynchronously by the queue thread.

		Args:
			type (str|Enum): Message type, typically a RemoteMessageType enum value
			**kwargs: Message payload data to serialize

		Note:
			This method is thread-safe and can be called from any thread.
			If the transport is not connected, the message will be silently dropped.
		"""
		obj = self.serializer.serialize(type=type, **kwargs)
		if self.connected:
			self.queue.put(obj)

	def _disconnect(self) -> None:
		"""Internal method to disconnect the transport.

		Cleans up the send queue thread, empties queued messages,
		and closes the socket connection.

		Note:
			This is called internally on errors, unlike close() which is called
			explicitly to shut down the transport.
		"""
		"""Disconnect the transport due to an error, without closing the connector thread."""
		if self.queue_thread is not None:
			self.queue.put(None)
			self.queue_thread.join()
			self.queue_thread = None
		clear_queue(self.queue)
		if self.serverSock:
			self.serverSock.close()
			self.serverSock = None

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
	    serializer (Serializer): Message serializer instance
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
	
	Args:
	    queue (Queue[Optional[bytes]]): Queue to clear
	"""
	try:
		while True:
			queue.get_nowait()
	except Exception:
		pass
