"""Thread-safe function execution in wxPython applications.

This module provides a decorator that ensures functions are executed safely
in the main GUI thread of a wxPython application. It wraps wxPython's CallAfter
mechanism in a convenient decorator form.

The module is particularly useful when:
- Functions need to update the GUI from background threads
- Methods are called from multiple threads and need thread-safe GUI access
- Events or callbacks might trigger GUI updates from non-main threads

Example:
    >>> from alwaysCallAfter import alwaysCallAfter
    >>> 
    >>> class MyFrame(wx.Frame):
    ...     @alwaysCallAfter
    ...     def update_status(self, text):
    ...         self.status.SetLabel(text)
    ...
    ...     def background_task(self):
    ...         # This is safe to call from any thread
    ...         self.update_status("Processing...")
"""

from functools import wraps
import wx


def alwaysCallAfter(func):
    """Ensure a function runs in the main GUI thread using wx.CallAfter.
    
    This decorator wraps any function to ensure it executes in the main
    wxPython GUI thread, regardless of which thread calls it. It uses
    wx.CallAfter to schedule the function execution for the next iteration
    of the event loop.
    
    Args:
        func (callable): The function to be wrapped. Can be an instance
            method or standalone function.
    
    Returns:
        callable: A wrapped version of the function that will always
            execute in the main GUI thread.
    
    Note:
        - The wrapped function will always execute asynchronously
        - Original function signature and documentation are preserved
        - Safe to use on methods that update GUI elements
        - Multiple decorated calls will be executed in order of scheduling
    
    Example:
        >>> @alwaysCallAfter
        ... def update_gui(text):
        ...     status_label.SetLabel(text)  # Safely updates GUI
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        wx.CallAfter(func, *args, **kwargs)
    return wrapper
