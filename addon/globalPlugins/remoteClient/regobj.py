##
##  Copyright 2009, Ryan Kelly (ryan@rfk.id.au)
##  Redistributable under the terms of the MIT license:
##
##    http://www.opensource.org/licenses/mit-license.php
##
"""

  regobj:  Pythonic object-based access to the Windows Registry

This module provides a thin wrapper around the standard _winreg module,
allowing easier and more pythonic access to the Windows Registry.

All access to the registry is done through Key objects, which (surprise!)
represent a specific registry key.  To begin, there are pre-existing Key
objects defined for the HKEY_* root keys, using both long and short names:

  >>> HKEY_CURRENT_USER
  <regobj Key 'HKEY_CURRENT_USER'>
  >>> HKLM
  <regobj Key 'HKEY_LOCAL_MACHINE'>

Traversing and creating subkeys is then as simple as ordinary python
attribute access:

  >>> HKCU.Software.Microsoft.Windows
  <regobj Key 'HKEY_CURRENT_USER\Software\Microsoft\Windows'>
  >>> HKCU.Software.MyTests
  Traceback (most recent call last):
      ...
  AttributeError: subkey 'MyTests' does not exist
  >>> HKCU.Software.MyTests = Key
  >>> HKCU.Software.MyTests
  <regobj Key 'HKEY_CURRENT_USER\Software\MyTests'>
  >>> del HKCU.Software.MyTests

Of course, for keys that don't happen to be named like python identifiers,
there are also methods that can accomplish the same thing.  To help reduce
visual clutter, calling a key object is a shorthand for attribute lookup:

  >>> HKCU.Software.set_subkey("my-funny-key",Key)
  >>> HKCU.Software.get_subkey("my-funny-key").SubKey = Key
  >>> HKCU("Software\\my-funny-key\\SubKey")
  <regobj Key 'HKEY_CURRENT_USER\Software\my-funny-key\SubKey'>
  >>> HKCU.Software.del_subkey("my-funny-key")

The individual values contained in a key can be accessed using standard
item access syntax.  The returned objects will be instances of the Value
class, with 'name', 'type' and 'data' attributes:

  >>> HKCU.Software.Microsoft.Clock["iFormat"]
  <regobj Value (iFormat,1,REG_SZ)>
  >>> HKCU.Software.Microsoft.Clock["iFormat"].name
  'iFormat'
  >>> print(HKCU.Software.Microsoft.Clock["iFormat"].data)
  1
  >>> print(type(HKCU.Software.Microsoft.Clock["iFormat"].data) is type(b'1'.decode('utf8')))
  True
  >>> HKCU.Software.Microsoft.Clock["iFormat"].type
  1
  >>> HKCU.Software.Microsoft.Clock["notavalue"]
  Traceback (most recent call last):
      ...
  KeyError: "no such value: 'notavalue'"
 
Iterating over a key generates all the contained values, followed by
all the contained subkeys.  There are also methods to seperately iterate
over just the values, and just the subkeys:

  >>> winK = HKCU.Software.Microsoft.Windows
  >>> winK["testvalue"] = 42
  >>> for obj in winK:
  ...   print(obj)
  <regobj Value (testvalue,42,REG_DWORD)>
  <regobj Key 'HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion'>
  <regobj Key 'HKEY_CURRENT_USER\Software\Microsoft\Windows\Shell'>
  <regobj Key 'HKEY_CURRENT_USER\Software\Microsoft\Windows\ShellNoRoam'>
  >>> [k.name for k in winK.subkeys()]
  ['CurrentVersion', 'Shell', 'ShellNoRoam']
  >>> [v.data for v in winK.values()]
  [42]
  >>> del winK["testvalue"]

These iterators also provide efficient implementations of the __contains__
and __len__ methods, so they can be used as follows:

  >>> "Shell" in HKCU.Software.Microsoft.Windows
  True
  >>> "Shell" in HKCU.Software.Microsoft.Windows.subkeys()
  True
  >>> "Shell" in HKCU.Software.Microsoft.Windows.values()
  False
  >>> len(HKCU.Software.Microsoft.Windows)
  3
  >>> len(HKCU.Software.Microsoft.Windows.values())
  0

Finally, there is powerful support for specifying key and value structures
at creation time.  The simplest case has already been demonstrated, where
setting a subkey to the Key class or to None will create it without any data:

  >>> HKCU.Software.MyTests = None
  >>> len(HKCU.Software.MyTests)
  0

If a subkey is assigned an existing key object, the data from that key is
copied into the subkey:

  >>> HKCU.Software.MyTests = HKCU.Software.Microsoft.Windows
  >>> len(HKCU.Software.MyTests)
  3
  >>> [k.name for k in HKCU.Software.MyTests]
  ['CurrentVersion', 'Shell', 'ShellNoRoam']
  >>> del HKCU.Software.MyTests

If a subkey is assigned a dictionary, the structure of that dictionary is
copied into the subkey.  Scalar values become key values, while nested 
dictionaries create subkeys:

  >>> HKCU.Software.MyTests = {"val1":7, "stuff":{"a":1,"c":2,"e":3}}
  >>> len(HKCU.Software.MyTests)
  2
  >>> [v.name for v in HKCU.Software.MyTests.values()]
  ['val1']
  >>> [k.name for k in HKCU.Software.MyTests.subkeys()]
  ['stuff']
  >>> len(HKCU.Software.MyTests.stuff)
  3
  >>> del HKCU.Software.MyTests

Any other value assigned to a subkey will become the default value for
that key (i.e. the value with name ""):

  >>> HKCU.Software.MyTests = "dead parrot"
  >>> print(HKCU.Software.MyTests[""].data)
  dead parrot
  >>> print(type(HKCU.Software.MyTests[""].data) is type(b'dead parrot'.decode('utf8')))
  True
  >>> del HKCU.Software.MyTests
 
And that's that - enjoy!

"""

__ver_major__ = 0
__ver_minor__ = 2
__ver_patch__ = 2
__ver_sub__ = ""
__version__ = "%d.%d.%d%s" % (__ver_major__,__ver_minor__,
                              __ver_patch__,__ver_sub__)

import sys
PY3 = sys.hexversion > 0x03000000

if PY3:
    import winreg as _winreg
else:
    import _winreg

# Import type constants into our namespace
TYPES = {}
TYPE_NAMES = ("REG_SZ","REG_RESOURCE_LIST","REG_NONE","REG_MULTI_SZ","REG_LINK",
              "REG_EXPAND_SZ","REG_DWORD_BIG_ENDIAN","REG_DWORD_LITTLE_ENDIAN",
              "REG_DWORD","REG_BINARY")
for nm in TYPE_NAMES:
    val = getattr(_winreg,nm)
    globals()[nm] = val
    TYPES[val] = nm


# Import SAM permission constants into our namespace
SAMS = {}
SAM_NAMES = ("KEY_ALL_ACCESS","KEY_CREATE_LINK","KEY_CREATE_SUB_KEY",
             "KEY_EXECUTE","KEY_NOTIFY","KEY_QUERY_VALUE","KEY_READ",
             "KEY_SET_VALUE","KEY_WRITE","KEY_ENUMERATE_SUB_KEYS")
for nm in SAM_NAMES:
    val = getattr(_winreg,nm)
    globals()[nm] = val
    SAMS[val] = nm


class Key(object):
    """Class representing a registry key.

    Each key has a name and a parent key object.  Its values can be
    accessed using standard item access syntax, while its subkeys can
    be accessed using standard attribute access syntax.

    Normally code would not create instance of this class directly.
    Rather, it would begin with one of the root key objects defined in
    this module (e.g. HKEY_CURRENT_USER) and then traverse it to load
    the appropriate key.
    """

    def __init__(self,name,parent,sam=KEY_READ,hkey=None):
        """Construct a new Key object.

        The key's name and parent key must be specified.  If the given
        name is a backslash-separated path it will be processed one 
        component at a time and the intermediate Key objects will be
        transparently instantiated.

        The optional argument 'sam' gives the security access mode to use
        for the key, defaulting to KEY_READ.  It more permissions are required
        for an attempted operation, we attempt to upgrade the permission
        automatically.

        If the optional argument 'hkey' is given, it is the underlying
        key id to be used when accessing the registry. This should really
        only be used for bootstrapping the root Key objects.
        """
        names = [nm for nm in name.split("\\") if nm]
        if len(names) == 0:
            raise ValueError("a non-empty key name is required")
        for pname in names[:-1]:
            parent = Key(pname,parent)
        self.name = names[-1]
        self.parent = parent
        self.sam = sam
        if hkey is not None:
            self.hkey = hkey

    def _get_hkey(self):
        try:
            return self.__dict__["hkey"]
        except KeyError:
            self.hkey = _winreg.OpenKey(self.parent.hkey,self.name,0,self.sam)
            return self.hkey

    def _del_hkey(self):
        if self.parent is not None:
            try:
                _winreg.CloseKey(self.__dict__["hkey"])
            except KeyError:
                pass
            try:
                del self.__dict__["hkey"]
            except KeyError:
                pass

    def get_subkey(self,name):
        """Retreive the subkey with the specified name.

        If the named subkey is not found, AttributeError is raised;
        this is for consistency with the attribute-based access notation.
        """
        subkey = Key(name,self)
        try:
            hkey = subkey.hkey
        except WindowsError:
            raise AttributeError("subkey '%s' does not exist" % (name,))
        return subkey

    def set_subkey(self,name,value=None):
        """Create the named subkey and set its value.

        There are several different ways to specify the new contents of
        the named subkey:

          * if 'value' is the Key class, a subclass thereof, or None, then
            the subkey is created but not populated with any data.
          * if 'value' is a key instance,  the data from that key will be
            copied into the new subkey.
          * if 'value' is a dictionary, the dict's keys are interpreted as
            key or value names and the corresponding entries are created
            within the new subkey - nested dicts create further subkeys,
            while scalar values create values on the subkey.
          * any other value will be converted to a Value object and assigned
            to the default value for the new subkey.

        """
        self.sam |= KEY_CREATE_SUB_KEY
        subkey = Key(name,self)
        try:
            subkey = self.get_subkey(name)
        except AttributeError:
            _winreg.CreateKey(self.hkey,name)
            subkey = self.get_subkey(name)
        if value is None:
            pass
        elif issubclass(type(value),type) and issubclass(value,Key):
            pass
        elif isinstance(value,Key):
            for v in value.values():
                subkey[v.name] = v
            for k in value.subkeys():
                subkey.set_subkey(k.name,k)
        elif isinstance(value,dict):
            for (nm,val) in value.items():
                if isinstance(val,dict):
                    subkey.set_subkey(nm,val)
                elif isinstance(val,Key):
                    subkey.set_subkey(nm,val)
                elif issubclass(type(val),type) and issubclass(val,Key):
                    subkey.set_subkey(nm,val)
                else:
                    subkey[nm] = val
        else:
            if not isinstance(value,Value):
                value = Value(value)
            subkey[value.name] = value

    def del_subkey(self,name):
        """Delete the named subkey, and any values or keys it contains."""
        self.sam |= KEY_WRITE
        subkey = self.get_subkey(name)
        subkey.clear()
        _winreg.DeleteKey(subkey.parent.hkey,subkey.name)

    def close(self):
        """Release underlying resources associated with this key."""
        del self.hkey

    def flush(self):
        """Ensure that the key's data is flushed to disk.

        Quoting the _winreg documentation:

          It is not necessary to call FlushKey() to change a key. Registry
          changes are flushed to disk by the registry using its lazy flusher.
          Registry changes are also flushed to disk at system shutdown. 
          Unlike CloseKey(), the FlushKey() method returns only when all the
          data has been written to the registry. An application should only
          call FlushKey() if it requires absolute certainty that registry
          changes are on disk.

          If you don't know whether a FlushKey() call is required, it
          probably isn't.

        """
        _winreg.FlushKey(self.hkey)

    def __eq__(self,key):
        try:
            return self.hkey == key.hkey
        except AttributeError:
            False

    def __str__(self):
        return "<regobj Key '%s'>" % (self.path,)

    def __repr__(self):
        return str(self)

    def __call__(self,name):
        """Calling accesses a subkey

        This is provided as a convenient shorthand for subkey names that
        are not valid python identifiers.
        """
        return self.get_subkey(name)

    def __getattr__(self,name):
        """Attribute access returns a subkey."""
        if name == "hkey":
            return self._get_hkey()
        elif name == "path":
            if self.parent is None:
                return self.name
            else:
                return self.parent.path + "\\" + self.name
        else:
            return self.get_subkey(name)

    def __setattr__(self,name,value):
        """Attribute assignment creates a new subkey."""
        if name == "sam":
            sam = self.__dict__.get("sam",0)
            if sam|value != sam:
                del self.hkey
            self.__dict__[name] = value
        elif name == "path":
            raise AttributeError("'path' cannot be set")
        elif name in ("name","parent","hkey",):
            self.__dict__[name] = value
        else:
            self.set_subkey(name,value)

    def __delattr__(self,name):
        """Deleting an attribute deletes the subkey."""
        if name == "hkey":
            self._del_hkey()
        else:
            self.del_subkey(name)

    def __getitem__(self,name):
        """Item access retrieves key values."""
        self.sam |= KEY_QUERY_VALUE
        try:
            data = _winreg.QueryValueEx(self.hkey,name)
        except WindowsError:
            raise KeyError("no such value: '%s'" % (name,))
        return Value(data[0],name,data[1])

    def __setitem__(self,name,value):
        """Item assignment sets key values."""
        self.sam |= KEY_SET_VALUE
        if not isinstance(value,Value):
            value = Value(value,name)
        _winreg.SetValueEx(self.hkey,name,0,value.type,value.data)

    def __delitem__(self,name):
        """Item deletion deletes key values."""
        self.sam |= KEY_SET_VALUE
        try:
            _winreg.DeleteValue(self.hkey,name)
        except WindowsError:
            raise KeyError("no such value: '%s'" % (name,))

    def __contains__(self,name):
        """A key contains a name if it has a matching subkey or value."""
        return (name in self.values() or name in self.subkeys())

    def __len__(self):
        """len() gives the number of values and subkeys."""
        info = _winreg.QueryInfoKey(self.hkey)
        return info[0] + info[1]

    def __iter__(self):
        """Default iteration is over both values and subkeys."""
        for v in self.values():
            yield v
        for k in self.subkeys():
            yield k

    def clear(self):
        """Remove all subkeys and values from this key."""    
        self.sam |= KEY_WRITE
        for v in list(self.values()):
            del self[v.name]
        for k in list(self.subkeys()):
            self.del_subkey(k.name)

    def subkeys(self):
        """Iterator over the subkeys of this key."""
        self.sam |= KEY_ENUMERATE_SUB_KEYS
        return SubkeyIterator(self)

    def values(self):
        """Iterator over the key's values."""
        return ValueIterator(self)


class Value(object):
    """Class representing registry key values.

    Each Value instance has a name, a type and some associated data.
    The default name is '', which corresponds to the default value for
    a registry key.  The type must be one of the REG_* constants from
    this module; if it is not specified, it will be guessed from the
    type of the data.
    """

    _DWORD_MAX_SIGNED = (1<<31) - 1
    _DWORD_MIN_SIGNED  = -1 * (1<<32)
    _DWORD_MAX_UNSIGNED = (1<<32) - 1

    def __init__(self,data=None,name="",type=None):
        if type is None:
            type = self._default_type(data)
        #  DWORD values are unsigned, but _winreg treats them as signed.
        #  We do some conversion on input so that unsigned values are
        #  accepted, but python will convert them into negative integers.
        #  when you read it back out :-(
        if data is not None and type == REG_DWORD:
            if data < self._DWORD_MIN_SIGNED:
                raise ValueError("DWORD value too small: %s" % (data,))
            elif data > self._DWORD_MAX_UNSIGNED:
                raise ValueError("DWORD value too large: %s" % (data,))
            elif data > self._DWORD_MAX_SIGNED:
                data = int(data - self._DWORD_MAX_UNSIGNED - 1)
        self.name = name
        self.data = data
        self.type = type

    def __str__(self):
        data = (self.name,self.data,TYPES[self.type])
        return "<regobj Value (%s,%s,%s)>" % data

    def __repr__(self):
       return str(self)

    def _default_type(self,data):
        if isinstance(data,int) or (not PY3 and isinstance(data,long)):
            return REG_DWORD
        if data is None:
            return REG_NONE
        return REG_SZ


class SubkeyIterator(object):
    """Iterator over the subkeys contained in a key.

    This iterator is capable of efficient membership detection
    and length reporting.  As usual, the underlying registry key
    should not be modified during iteration.
    """

    def __init__(self,key):
        self.key = key
        self.index = 0

    def __len__(self):
        return _winreg.QueryInfoKey(self.key.hkey)[0]

    def __contains__(self,name):
        try:
            self.key(name)
        except AttributeError:
            return False
        return True

    def __iter__(self):
        return self

    def next(self):
        try:
            k = _winreg.EnumKey(self.key.hkey,self.index)
        except WindowsError:
            raise StopIteration
        else:
            self.index += 1
            return Key(k,self.key)
    __next__ = next
        

class ValueIterator(object):
    """Iterator over the values contained in a key.

    This iterator is capable of efficient membership detection
    and length reporting.  As usual, the underlying registry key
    should not be modified during iteration.
    """

    def __init__(self,key):
        self.key = key
        self.index = 0

    def __len__(self):
        return _winreg.QueryInfoKey(self.key.hkey)[1]

    def __contains__(self,name):
        try:
            self.key[name]
        except KeyError:
            return False
        return True

    def __iter__(self):
        return self

    def next(self):
        try:
            v = _winreg.EnumValue(self.key.hkey,self.index)
        except WindowsError:
            raise StopIteration
        else:
            self.index += 1
            return Value(v[1],v[0],v[2])
    __next__ = next


# Bootstrap by creating constants for the root keys

HKCR = Key("HKEY_CLASSES_ROOT",None,KEY_READ,_winreg.HKEY_CLASSES_ROOT)
HKEY_CLASSES_ROOT = HKCR

HKCC = Key("HKEY_CURRENT_CONFIG",None,KEY_READ,_winreg.HKEY_CURRENT_CONFIG)
HKEY_CURRENT_CONFIG = HKCC

HKCU = Key("HKEY_CURRENT_USER",None,KEY_READ,_winreg.HKEY_CURRENT_USER)
HKEY_CURRENT_USER = HKCU

HKDD = Key("HKEY_DYN_DATA",None,KEY_READ,_winreg.HKEY_DYN_DATA)
HKEY_DYN_DATA = HKDD

HKLM = Key("HKEY_LOCAL_MACHINE",None,KEY_READ,_winreg.HKEY_LOCAL_MACHINE)
HKEY_LOCAL_MACHINE = HKLM

HKPD = Key("HKEY_PERFORMANCE_DATA",None,KEY_READ,_winreg.HKEY_PERFORMANCE_DATA)
HKEY_PERFORMANCE_DATA = HKPD

HKU = Key("HKEY_USERS",None,KEY_READ,_winreg.HKEY_USERS)
HKEY_USERS = HKU


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)

