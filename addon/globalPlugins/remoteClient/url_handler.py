try:
	from logHandler import log
except ImportError:
	from logging import getLogger
	log = getLogger('url_handler')

import ctypes
import os
import win32con
import regobj
import connection_info

import windowUtils
import wx

class COPYDATASTRUCT(ctypes.Structure):
	_fields_ = [
		('dwData', ctypes.wintypes.LPARAM),
		('cbData', ctypes.wintypes.DWORD),
		('lpData', ctypes.c_void_p)
	]

PCOPYDATASTRUCT = ctypes.POINTER(COPYDATASTRUCT)

class URLHandlerWindow(windowUtils.CustomWindow):
	className = u'NVDARemoteURLHandler'

	def __init__(self, callback=None, *args, **kwargs):
		super(URLHandlerWindow, self).__init__(*args, **kwargs)
		self.callback = callback


	def windowProc(self, hwnd, msg, wParam, lParam):
		if msg != win32con.WM_COPYDATA:
			return
		hwnd = wParam
		struct_pointer = lParam
		message_data = ctypes.cast(struct_pointer, PCOPYDATASTRUCT)
		url = ctypes.wstring_at(message_data.contents.lpData)
		log.info("Received url: %s" % url)
		try:
			con_info = connection_info.ConnectionInfo.from_url(url)
		except connection_info.URLParsingError:
			log.exception("unable to parse nvdaremote:// url %s" % url)
			raise
		log.info("Connection info: %r" % con_info)
		if callable(self.callback):
			wx.CallLater(50, self.callback, con_info)

def register_url_handler():
	regobj.HKCU.SOFTWARE.Classes.nvdaremote = URL_HANDLER_REGISTRY

def unregister_url_handler():
	del regobj.HKCU.SOFTWARE.Classes.nvdaremote 

def url_handler_path():
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

