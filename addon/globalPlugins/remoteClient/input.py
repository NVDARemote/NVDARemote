import ctypes.wintypes as ctypes
import braille
import brailleInput
import globalPluginHandler
import scriptHandler
import inputCore
import api

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2
MAPVK_VK_TO_VSC = 0
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENT_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004

class MOUSEINPUT(ctypes.Structure):
	_fields_ = (
		('dx', ctypes.c_long),
		('dy', ctypes.c_long),
		('mouseData', ctypes.DWORD),
		('dwFlags', ctypes.DWORD),
		('time', ctypes.DWORD),
		('dwExtraInfo', ctypes.POINTER(ctypes.c_ulong)),
	)

class KEYBDINPUT(ctypes.Structure):
	_fields_ = (
		('wVk', ctypes.WORD),
		('wScan', ctypes.WORD),
		('dwFlags', ctypes.DWORD),
		('time', ctypes.DWORD),
		('dwExtraInfo', ctypes.POINTER(ctypes.c_ulong)),
	)

class HARDWAREINPUT(ctypes.Structure):
	_fields_ = (
		('uMsg', ctypes.DWORD),
		('wParamL', ctypes.WORD),
		('wParamH', ctypes.WORD),
	)

class INPUTUnion(ctypes.Union):
	_fields_ = (
		('mi', MOUSEINPUT),
		('ki', KEYBDINPUT),
		('hi', HARDWAREINPUT),
	)

class INPUT(ctypes.Structure):
	_fields_ = (
		('type', ctypes.DWORD),
		('union', INPUTUnion))

class BrailleInputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):

	def __init__(self, **kwargs):
		super(BrailleInputGesture, self).__init__()
		for key, value in kwargs.iteritems():
			setattr(self, key, value)
		self.source="remote{}{}".format(self.source[0].upper(),self.source[1:])
		self.scriptPath=getattr(self,"scriptPath",None)
		self.script=self.findScript() if self.scriptPath else None

	def findScript(self):
		if not (isinstance(self.scriptPath,list) and len(self.scriptPath)==3):
			return None
		module,cls,scriptName=self.scriptPath
		focus = api.getFocusObject()
		if not focus:
			return None
		if scriptName.startswith("kb:"):
			# Emulate a key press.
			return scriptHandler._makeKbEmulateScript(scriptName)

		import globalCommands

		# Global plugin level.
		if cls=='GlobalPlugin':
			for plugin in globalPluginHandler.runningPlugins:
				if module==plugin.__module__:
					func = getattr(plugin, "script_%s" % scriptName, None)
					if func:
						return func

		# App module level.
		app = focus.appModule
		if app and cls=='AppModule' and module==app.__module__:
			func = getattr(app, "script_%s" % scriptName, None)
			if func:
				return func

		# Tree interceptor level.
		treeInterceptor = focus.treeInterceptor
		if treeInterceptor and treeInterceptor.isReady:
			func = getattr(treeInterceptor , "script_%s" % scriptName, None)
			if func:
				return func

		# NVDAObject level.
		func = getattr(focus, "script_%s" % scriptName, None)
		if func:
			return func
		for obj in reversed(api.getFocusAncestors()):
			func = getattr(obj, "script_%s" % scriptName, None)
			if func and getattr(func, 'canPropagate', False):
				return func

		# Global commands.
		func = getattr(globalCommands.commands, "script_%s" % scriptName, None)
		if func:
			return func

		return None

def send_key(vk=None, scan=None, extended=False, pressed=True):
	i = INPUT()
	i.union.ki.wVk = vk
	if scan:
		i.union.ki.wScan = scan
	else: #No scancode provided, try to get one
		i.union.ki.wScan = ctypes.windll.user32.MapVirtualKeyW(vk, MAPVK_VK_TO_VSC)
	if not pressed:
		i.union.ki.dwFlags |= KEYEVENTF_KEYUP 
	if extended:
		i.union.ki.dwFlags |= KEYEVENTF_EXTENDEDKEY
	i.type = INPUT_KEYBOARD
	ctypes.windll.user32.SendInput(1, ctypes.byref(i), ctypes.sizeof(INPUT))
