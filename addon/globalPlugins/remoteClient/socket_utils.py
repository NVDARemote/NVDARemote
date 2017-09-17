import urlparse

SERVER_PORT = 6837

def address_to_hostport(addr):
	"""Converts an address such as google.com:80 into an address adn port tuple.
	If no port is given, use SERVER_PORT."""
	addr = urlparse.urlparse('//'+addr)
	port = addr.port or SERVER_PORT
	if addr.hostname.find(":")!=-1 and addr.netloc.startswith("["): # This is an IPV6 address
		return (addr.hostname, port, 0, 0)
	else:
		return (addr.hostname, port)

def hostport_to_address(hostport):
	if len(hostport)==4:
		host, port, flow, scope=hostport
		if port != SERVER_PORT:
			return "["+host+"]:"+str(port)
		return "["+host+"]"
	else:
		host, port = hostport
	if port != SERVER_PORT:
		return host+':'+str(port)
	return host
