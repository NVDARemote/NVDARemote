import urllib
import urlparse
import socket_utils

URL_PREFIX = 'nvdaremote://'

class URLParsingError(Exception):
	"""Raised if it's impossible to parse out the URL"""

class ConnectionInfo(object):

	def __init__(self, hostname, mode, key, port=socket_utils.SERVER_PORT):
		self.hostname = hostname
		self.mode = mode
		self.key = key
		self.port = port or socket_utils.SERVER_PORT

	@classmethod
	def from_url(cls, url):
		parsed_url = urlparse.urlparse(url)
		parsed_query = urlparse.parse_qs(parsed_url.query)
		hostname = parsed_url.hostname
		port = parsed_url.port
		key = parsed_query.get('key', [""])[0]
		mode = parsed_query.get('mode', [""])[0].lower()
		if not hostname:
			raise URLParsingError("No hostname provided")
		if not key:
			raise URLParsingError(_("No key provided"))
		if not mode:
			raise URLParsingError(_("No mode provided"))
		if mode not in ('master', 'slave'):
			raise URLParsingError(_("Invalud mode provided: %r" % mode))
		return cls(hostname=hostname, mode=mode, key=key, port=port)

	def __repr__(self):
		return "{classname} (hostname={hostname}, port={port}, mode={mode}, key={key})".format(classname=self.__class__.__name__, hostname=self.hostname, port=self.port, mode=self.mode, key=self.key)

	def get_address(self):
		return '{hostname}:{port}'.format(hostname=self.hostname, port=self.port)

	def get_url_to_connect(self):
		result = URL_PREFIX + self.hostname
		if self.port != socket_utils.SERVER_PORT:
			result += ':{port}'.format(port=self.port)
		result += '?'
		mode = self.mode
		if mode == 'master':
			mode = 'slave'
		elif mode == 'slave':
			mode = 'master'
		result += urllib.urlencode(dict(key=self.key, mode=mode))
		return result

	def get_url(self):
		result = URL_PREFIX + self.hostname
		if self.port != socket_utils.SERVER_PORT:
			result += ':{port}'.format(port=self.port)
		result += '?'
		mode = self.mode
		result += urllib.urlencode(dict(key=self.key, mode=mode))
		return result
