import urlparse
import socket_utils

class URLParsingError(Exception):
	"""Raised if it's impossible to parse out the URL"""\

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
		key = parsed_query.get('key')
		mode = parsed_query.get('mode')
		if not hostname:
			raise URLParsingError("No hostname provided")
		if not key:
			raise URLParsingError("No key provided")
		if not mode:
			raise URLParsingError("No mode provided")
		return cls(hostname=hostname, mode=mode[0], key=key[0], port=port)

	def __repr__(self):
		return "{classname} (hostname={hostname}, port={port}, mode={mode}, key={key})".format(classname=self.__class__.__name__, hostname=self.hostname, port=self.port, mode=self.mode, key=self.key)

	def get_address(self):
		return '{hostname}:{port}'.format(hostname=self.hostname, port=self.port)
