import urlparse

SERVER_PORT = 6837

def address_to_hostport(addr):
	"""Converts an address such as google.com:80 into an address adn port tuple.
	If no port is given, use SERVER_PORT."""
	addr = urlparse.urlparse('//'+addr)
	port = addr.port or SERVER_PORT
	return (addr.hostname, port)

def hostport_to_address(hostport):
	host, port = hostport
	if ':' in host:
		host = '[' + host + ']'
	if port != SERVER_PORT:
		return host+':'+str(port)
	return host
