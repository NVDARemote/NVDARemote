"""Decorator for thread-safe GUI updates in wxPython.

Ensures decorated functions run in the main GUI thread using wx.CallAfter,
which is necessary when updating the interface from background threads.
"""

from functools import wraps

import wx


def alwaysCallAfter(func):
    """Decorator that makes functions thread-safe for GUI updates.
    
    Args:
        func: The function to wrap
    
    Returns:
        A wrapped version that always executes in the main thread
    
    Example:
        @alwaysCallAfter
        def update_label(text):
            label.SetLabel(text)  # Safely updates GUI from any thread
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        wx.CallAfter(func, *args, **kwargs)
    return wrapper
