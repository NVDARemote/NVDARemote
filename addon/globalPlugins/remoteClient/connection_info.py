from urllib.parse import parse_qs, urlencode, urlparse


from .protocol import SERVER_PORT, URL_PREFIX

from . import socket_utils

class URLParsingError(Exception):
	"""Raised if it's impossible to parse out the URL"""

class ConnectionInfo:

	def __init__(self, hostname, mode, key, port=SERVER_PORT):
		self.hostname = hostname
		self.mode = mode
		self.key = key
		self.port = port or SERVER_PORT

	@classmethod
	def fromURL(cls, url):
		parsedUrl = urlparse(url)
		parsedQuery = parse_qs(parsedUrl.query)
		hostname = parsedUrl.hostname
		port = parsedUrl.port
		key = parsedQuery.get('key', [""])[0]
		mode = parsedQuery.get('mode', [""])[0].lower()
		if not hostname:
			raise URLParsingError("No hostname provided")
		if not key:
			raise URLParsingError("No key provided")
		if not mode:
			raise URLParsingError("No mode provided")
		if mode not in ('master', 'slave'):
			raise URLParsingError("Invalud mode provided: %r" % mode)
		return cls(hostname=hostname, mode=mode, key=key, port=port)

	def __repr__(self):
		return "{classname} (hostname={hostname}, port={port}, mode={mode}, key={key})".format(classname=self.__class__.__name__, hostname=self.hostname, port=self.port, mode=self.mode, key=self.key)

	def getAddress(self):
		hostname = (self.hostname if ':' not in self.hostname else '[' + self.hostname + ']')
		return '{hostname}:{port}'.format(hostname=hostname, port=self.port)

	def getURLToConnect(self):
		result = URL_PREFIX + socket_utils.hostPortToAddress((self.hostname, self.port))
		result += '?'
		mode = self.mode
		if mode == 'master':
			mode = 'slave'
		elif mode == 'slave':
			mode = 'master'
		result += urlencode(dict(key=self.key, mode=mode))
		return result

	def getURL(self):
		result = URL_PREFIX + socket_utils.hostPortToAddress((self.hostname, self.port))
		result += '?'
		mode = self.mode
		result += urlencode(dict(key=self.key, mode=mode))
		return result
