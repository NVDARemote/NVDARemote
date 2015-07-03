import threading
import time
import Queue
import ssl
import socket
import select
from collections import defaultdict
from logging import getLogger
log = getLogger('transport')
import callback_manager

class Transport(object):

	def __init__(self, serializer):
		self.serializer = serializer
		self.callback_manager = callback_manager.CallbackManager()
		self.connected = False
		self.successful_connects = 0

	def transport_connected(self):
		self.successful_connects += 1
		self.connected = True
		self.callback_manager.call_callbacks('transport_connected')

class TCPTransport(Transport):

	def __init__(self, serializer, address, timeout=0):
		super(TCPTransport, self).__init__(serializer=serializer)
		self.closed = False
		#Buffer to hold partially received data
		self.buffer = ""
		self.queue = Queue.Queue()
		self.address = address
		self.server_sock = None
		self.queue_thread = None
		self.timeout = timeout

	def run(self):
		self.closed = False
		self.server_sock = self.create_server_socket()
		try:
			self.server_sock.connect(self.address)
		except Exception as e:
			self.callback_manager.call_callbacks('transport_connection_failed')
			raise
		self.transport_connected()
		self.queue_thread = threading.Thread(target=self.send_queue)
		self.queue_thread.daemon = True
		self.queue_thread.start()
		while not self.closed:
			try:
				readers, writers, error = select.select([self.server_sock], [], [self.server_sock])
			except socket.error:
				self.buffer = ""
				break
			if self.server_sock in error:
				self.buffer = ""
				break
			if self.server_sock in readers:
				try:
					self.handle_server_data()
				except socket.error:
					self.buffer = ""
					break
		self.connected = False
		self.callback_manager.call_callbacks('transport_disconnected')
		self.close()

	def create_server_socket(self):
		server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if self.timeout:
			server_sock.settimeout(self.timeout)
		server_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		server_sock.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60000, 2000))
		server_sock = ssl.wrap_socket(server_sock)
		return server_sock

	def handle_server_data(self):
		data = self.buffer + self.server_sock.recv(8192)
		self.buffer = ""
		if data == '':
			self.close()
			return
		if '\n' not in data:
			self.buffer += data
			return
		while '\n' in data:
			line, sep, data = data.partition('\n')
			self.parse(line)
		self.buffer += data

	def parse(self, line):
		obj = self.serializer.deserialize(line)
		if 'type' not in obj:
			return
		callback = "msg_"+obj['type']
		del obj['type']
		self.callback_manager.call_callbacks(callback, **obj)

	def send_queue(self):
		while True:
			item = self.queue.get()
			if item is None:
				return
			try:
				self.server_sock.sendall(item)
			except socket.error:
				return

	def send(self, type, **kwargs):
		obj = self.serializer.serialize(type=type, **kwargs)
		if self.connected:
			self.queue.put(obj)

	def close(self):
		if self.closed:
			return
		self.callback_manager.call_callbacks('transport_closing')
		self.closed = True
		if self.queue_thread is not None:
			self.queue.put(None)
			self.queue_thread.join()
		clear_queue(self.queue)
		self.server_sock.close()
		self.server_sock = None

class RelayTransport(TCPTransport):

	def __init__(self, serializer, address, timeout=0, channel=None):
		super(RelayTransport, self).__init__(address=address, serializer=serializer, timeout=timeout)
		log.info("Connecting to %s channel %s" % (address, channel))
		self.channel = channel
		self.callback_manager.register_callback('transport_connected', self.on_connected)

	def on_connected(self):
		if self.channel is not None:
			self.send('join', channel=self.channel)
		else:
			self.send('generate_key')

class ConnectorThread(threading.Thread):

	def __init__(self, connector, connect_delay=5):
		super(ConnectorThread, self).__init__()
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

def clear_queue(queue):
	try:
		while True:
			queue.get_nowait()
	except:
		pass
