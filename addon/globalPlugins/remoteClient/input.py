import ctypes.wintypes as ctypes

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
