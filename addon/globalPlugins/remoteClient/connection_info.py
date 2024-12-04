from dataclasses import dataclass
from urllib.parse import parse_qs, urlencode, urlparse

from .protocol import SERVER_PORT, URL_PREFIX
from . import socket_utils

class URLParsingError(Exception):
	"""Raised if it's impossible to parse out the URL"""

@dataclass
class ConnectionInfo:
	hostname: str
	mode: str
	key: str
	port: int = SERVER_PORT

	def __post_init__(self):
		self.port = self.port or SERVER_PORT

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


	def getAddress(self):
		# Handle IPv6 addresses by adding brackets if needed
		hostname = f'[{self.hostname}]' if ':' in self.hostname else self.hostname
		return f'{hostname}:{self.port}'

	def _build_url(self, mode):
		# Build URL components
		netloc = socket_utils.hostPortToAddress((self.hostname, self.port))
		query = urlencode({'key': self.key, 'mode': mode})
		
		# Use urlunparse for proper URL construction
		return urlparse.urlunparse((
			URL_PREFIX.split('://')[0],  # scheme from URL_PREFIX
			netloc,        # network location
			'',           # path
			'',           # params
			query,        # query string
			''            # fragment
		))

	def getURLToConnect(self):
		# Flip master/slave for connection URL
		connect_mode = 'slave' if self.mode == 'master' else 'master'
		return self._build_url(connect_mode)

	def getURL(self):
		return self._build_url(self.mode)
