from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import urllib.parse

SERVER_PORT = 6837

def address_to_hostport(addr):
	"""Converts an address such as google.com:80 into an address adn port tuple.
	If no port is given, use SERVER_PORT."""
	addr = urllib.parse.urlparse('//'+addr)
	port = addr.port or SERVER_PORT
	return (addr.hostname, port)

def hostport_to_address(hostport):
	host, port = hostport
	if ':' in host:
		host = '[' + host + ']'
	if port != SERVER_PORT:
		return host+':'+str(port)
	return host
