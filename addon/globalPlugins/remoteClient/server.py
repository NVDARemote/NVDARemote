import os
import select
import socket
import ssl
import sys
try:
	import json
except ImportError:
	sys.path.append(os.path.abspath(os.path.dirname(__file__)))
	import json
	sys.path.remove(sys.path[-1])
import time

class Server(object):
	PING_TIME = 300

	def __init__(self, port, password, bind_host=''):
		self.port = port
		self.password = password
		#Maps client sockets to clients
		self.clients = {}
		self.client_sockets = []
		self.running = False
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		certfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'server.pem')
		self.server_socket = ssl.wrap_socket(self.server_socket, certfile=certfile)
		self.server_socket.bind((bind_host, self.port))
		self.server_socket.listen(5)

	def run(self):
		self.running = True
		self.last_ping_time = time.time()
		while self.running:
			r, w, e = select.select(self.client_sockets+[self.server_socket], [], self.client_sockets, 60)
			if not self.running:
				break
			for sock in r:
				if sock is self.server_socket:
					self.accept_new_connection()
					continue
				self.clients[sock].handle_data()
			if time.time() - self.last_ping_time >= self.PING_TIME:
				for client in self.clients.itervalues():
					if client.authenticated:
						client.send(type='ping')
				self.last_ping_time = time.time()

	def accept_new_connection(self):
		try:
			client_sock, addr = self.server_socket.accept()
		except ssl.SSLError:
			return
		client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		client = Client(server=self, socket=client_sock)
		self.add_client(client)

	def add_client(self, client):
		self.clients[client.socket] = client
		self.client_sockets.append(client.socket)

	def remove_client(self, client):
		del self.clients[client.socket]
		self.client_sockets.remove(client.socket)

	def client_disconnected(self, client):
		self.remove_client(client)
		if client.authenticated:
			client.send_to_others(type='client_left', user_id=client.id, client=client.as_dict())

	def close(self):
		self.running = False
		self.server_socket.close()

class Client(object):
	id = 0

	def __init__(self, server, socket):
		self.server = server
		self.socket = socket
		self.buffer = ""
		self.authenticated = False
		self.id = Client.id + 1
		self.connection_type = None
		self.protocol_version = 1
		Client.id += 1

	def handle_data(self):
		try:
			data = self.buffer + self.socket.recv(16384)
		except:
			self.close()
			return
		if data == '': #Disconnect
			self.close()
			return
		if '\n' not in data:
			self.buffer = data
			return
		self.buffer = ""
		while '\n' in data:
			line, sep, data = data.partition('\n')
			self.parse(line)
		self.buffer += data

	def parse(self, line):
		try:
			parsed = json.loads(line)
		except ValueError:
			self.close()
			return
		if 'type' not in parsed:
			return
		if self.authenticated:
			self.send_to_others(**parsed)
			return
		fn = 'do_'+parsed['type']
		if hasattr(self, fn):
			getattr(self, fn)(parsed)

	def as_dict(self):
		return dict(id=self.id, connection_type=self.connection_type)

	def do_join(self, obj):
		password = obj.get('channel', None)
		if password != self.server.password:
			self.send(type='error', message='incorrect_password')
			self.close()
			return
		self.connection_type = obj.get('connection_type')
		self.authenticated = True
		clients = []
		client_ids = []
		for c in self.server.clients.values():
			if c is self or not c.authenticated:
				continue
			clients.append(c.as_dict())
			client_ids.append(c.id)
		self.send(type='channel_joined', channel=self.server.password, user_ids=client_ids, clients=clients)
		self.send_to_others(type='client_joined', user_id=self.id, client=self.as_dict())

	def do_protocol_version(self, obj):
		version = obj.get('version')
		if not version:
			return
		self.protocol_version = version

	def close(self):
		self.socket.close()
		self.server.client_disconnected(self)

	def send(self, type, origin=None, clients=None, client=None, **kwargs):
		msg = dict(type=type, **kwargs)
		if self.protocol_version > 1:
			if origin:
				msg['origin'] = origin
			if clients:
				msg['clients'] = clients
			if client:
				msg['client'] = client
		msgstr = json.dumps(msg)+"\n"
		try:
			self.socket.sendall(msgstr)
		except:
			self.close()

	def send_to_others(self, origin=None, **obj):
		if origin is None:
			origin = self.id
		for c in self.server.clients.itervalues():
			if c is not self and c.authenticated:
				c.send(origin=origin, **obj)
