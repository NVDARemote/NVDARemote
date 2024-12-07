from functools import wraps

import wx


def alwaysCallAfter(func):
	"""Decorator to call a function after the current event loop has finished."""
	@wraps(func)
	def wrapper(*args, **kwargs):
		wx.CallAfter(func, *args, **kwargs)
	return wrapper
