"""
URL Handler Module
=================

This module implements Windows protocol handler registration and message handling for
nvdaremote:// URLs. It enables NVDA Remote to be launched via custom URLs that specify
connection parameters.

The module provides:
- A custom window class to receive and parse URLs via Windows messages
- Registry management for the nvdaremote:// protocol
- Utilities for protocol handler registration and cleanup

The URL handler allows users to connect to NVDA Remote sessions by clicking links
or entering URLs in the format:
    nvdaremote://<host>:<port>/<mode>/<key>

Example:
    >>> register_url_handler()  # Register protocol in Windows
    >>> window = URLHandlerWindow(callback=handle_connection)
    >>> # Now nvdaremote:// URLs will be handled
    >>> unregister_url_handler()  # Clean up when done
"""

try:
	from logHandler import log
except ImportError:
	from logging import getLogger
	log = getLogger('url_handler')

import ctypes
import ctypes.wintypes
import os

import gui  # provided by NVDA
import windowUtils
import wx
from winUser import WM_COPYDATA  # provided by NVDA

from . import connection_info, regobj


class COPYDATASTRUCT(ctypes.Structure):
	"""Windows COPYDATASTRUCT for inter-process communication.
	
	This structure is used by Windows to pass data between processes using
	the WM_COPYDATA message. It contains fields for:
	- Custom data value (dwData)
	- Size of data being passed (cbData)
	- Pointer to the actual data (lpData)
	"""
	
	_fields_ = [
		('dwData', ctypes.wintypes.LPARAM),
		('cbData', ctypes.wintypes.DWORD),
		('lpData', ctypes.c_void_p)
	]


PCOPYDATASTRUCT = ctypes.POINTER(COPYDATASTRUCT)

MSGFLT_ALLOW = 1


class URLHandlerWindow(windowUtils.CustomWindow):
	"""Window class that receives and processes nvdaremote:// URLs.
	
	This window registers itself to receive WM_COPYDATA messages containing
	URLs. When a URL is received, it:
	1. Parses the URL into connection parameters
	2. Validates the URL format
	3. Calls the provided callback with the connection info
	
	The window automatically handles UAC elevation by allowing messages
	from lower privilege processes.
	"""
	
	className = u'NVDARemoteURLHandler'

	def __init__(self, callback=None, *args, **kwargs):
		"""Initialize URL handler window.
		
		Args:
			callback (callable, optional): Function to call with parsed ConnectionInfo
				when a valid URL is received. Defaults to None.
			*args: Additional arguments passed to CustomWindow
			**kwargs: Additional keyword arguments passed to CustomWindow
		"""
		super().__init__(*args, **kwargs)
		self.callback = callback
		try:
			ctypes.windll.user32.ChangeWindowMessageFilterEx(
				self.handle, WM_COPYDATA, MSGFLT_ALLOW, None)
		except AttributeError:
			pass

	def windowProc(self, hwnd, msg, wParam, lParam):
		"""Windows message procedure for handling received URLs.
		
		Processes WM_COPYDATA messages containing nvdaremote:// URLs.
		Parses the URL and calls the callback if one was provided.
		
		Args:
			hwnd: Window handle
			msg: Message type
			wParam: Source window handle
			lParam: Pointer to COPYDATASTRUCT containing the URL
			
		Raises:
			URLParsingError: If the received URL is malformed or invalid
		"""
		if msg != WM_COPYDATA:
			return
		hwnd = wParam
		struct_pointer = lParam
		message_data = ctypes.cast(struct_pointer, PCOPYDATASTRUCT)
		url = ctypes.wstring_at(message_data.contents.lpData)
		log.info("Received url: %s" % url)
		try:
			con_info = connection_info.ConnectionInfo.fromURL(url)
		except connection_info.URLParsingError:
			wx.CallLater(50, gui.messageBox, parent=gui.mainFrame, caption=_("Invalid URL"),
						 # Translators: Message shown when an invalid URL has been provided.
						 message=_("Unable to parse url \"%s\"") % url, style=wx.OK | wx.ICON_ERROR)
			log.exception("unable to parse nvdaremote:// url %s" % url)
			raise
		log.info("Connection info: %r" % con_info)
		if callable(self.callback):
			wx.CallLater(50, self.callback, con_info)


def register_url_handler():
	"""Register the nvdaremote:// protocol handler in the Windows registry.
	
	Creates registry entries under HKEY_CURRENT_USER to associate the
	nvdaremote:// protocol with this addon's URL handler executable.
	This allows Windows to launch NVDA Remote when nvdaremote:// URLs
	are activated.
	"""
	regobj.HKCU.SOFTWARE.Classes.nvdaremote = URL_HANDLER_REGISTRY


def unregister_url_handler():
	"""Remove the nvdaremote:// protocol handler from the Windows registry.
	
	Cleans up registry entries created by register_url_handler().
	Should be called when uninstalling or updating the addon.
	"""
	del regobj.HKCU.SOFTWARE.Classes.nvdaremote


def url_handler_path():
	"""Get the full path to the URL handler executable.
	
	Returns:
		str: Absolute path to url_handler.exe in the addon directory
	"""
	return os.path.join(os.path.split(os.path.abspath(__file__))[0], 'url_handler.exe')


URL_HANDLER_REGISTRY = {
	"URL Protocol": "",
	"shell": {
		"open": {
			"command": {
					"": '"{path}" %1'.format(path=url_handler_path()),
			}
		}
	}
}
