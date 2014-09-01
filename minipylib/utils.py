# -*- coding: utf-8 -*-
"""
minipylib.utils

Utility functions.

* created: 2011-04-17 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-31 kchan
"""

from __future__ import (absolute_import, unicode_literals, print_function)

import six
import os
import sys
import hashlib
import codecs
import string
import logging



# add directory to module search path (sys.path)

def add_to_sys_path(path, append=False):
    """
    Add directory to ``sys.path``.
    * This function will add the path only if it's not already in sys.path.

    :param path: module directory to add to ``sys.path``.
    :param append: if True, append to sys.path, else insert.
    """
    if os.path.isdir(path) and not path in sys.path:
        if append:
            sys.path.append(path)
        else:
            sys.path.insert(1, path)


# import module given path

def import_module(path, module_name=None):
    """
    Import module from path.
    * based on code from the following:
    http://stackoverflow.com/questions/1096216/override-namespace-in-python

    :param path: full path to module to import
    :param module_name: name to map module in sys.modules
    :returns: imported module
    """
    if not module_name:
        m = hashlib.sha1()
        m.update(path)
        module_name = m.hexdigest()
    sys.path.insert(0, os.path.dirname(path))
    try:
        mod_path, ext = os.path.splitext(os.path.basename(path))
        module = __import__(mod_path)
        sys.modules[module_name] = module
    finally:
        sys.path.pop(0)
    return module


# old version

# def import_module(path):
#     """
#     Dynamically import module from path and return a module object.
#
#     :param path: file path of module to import.
#     :returns: module or `None` if error.
#
#     :FIXME: This will not work in Python 3 (esp. >= Python 3.4) since
#     the imp module is deprecated. Need to rewrite.
#     """
#     try:
#         assert path is not None and os.path.isfile(path)
#         src = open(path, 'rb')
#         m = hashlib.sha1()
#         m.update(path)
#         module = imp.load_source(m.hexdigest(), path, src)
#         src.close()
#     except (TypeError, AssertionError, IOError):
#         module = None
#     return module


# import vars from modules

def import_module_vars(module, varnames=None):
    """
    Import vars from module.

    Example::

        data = import_module_vars('webapp.urls', 'URLS')

    :More info: `<http://stackoverflow.com/questions/2259427/load-python-code-at-runtime>`_

    :param module: module name.
    :param varnames: list of vars to import (defaults to None)
    :returns: None on error, otherwise `dict` of name/values. If no `args`,
        return module `__dict__`.
    """
    try:
        m = __import__(module, globals(), locals(), varnames, -1)
    except ImportError:
        return None

    if module.find('.') != -1:
        # submodule
        m = sys.modules[module]

    if varnames is None or len(varnames) == 0:
        result = m.__dict__
    else:
        result = {}
        for name in varnames:
            try:
                result[name] = getattr(m, name)
            except AttributeError:
                pass
    return result


def import_module_settings(module):
    """
    Import settings from module.

    * only global vars in ALL CAPS are imported.

    :param module: name of module to import from.
    :returns: imported settings or `None` on error.
    """
    data = import_module_vars(module)
    try:
        settings = dict([(k, v) for k, v in data.items() if k == k.upper()])
    except AttributeError:
        return None
    return settings


# create class instance based on module and class name

def get_instance(module, class_name, *args, **kwargs):
    """
    Return an instance of the object based on module name and class name.

    :param module: module name.
    :param class_name: name of class to instantiate.
    :param args: args to pass to class.
    :param kwargs: keyword args to pass to class.
    :returns: instance of class.
    """
    __import__(module)
    f = getattr(sys.modules[module], class_name)
    return f(*args, **kwargs)


# file read/write/delete helper functions

default_text_encoding = "utf-8"
default_encoding = default_text_encoding

def open_file(path, mode=None, encoding=None, **kwargs):
    """
    Helper function to open a file for reading/writing.

    :param path: path of file to read.
    :param mode: "b" for bytes or "t" for text (default is "t")
    :param encoding: file encoding for text (default is `utf-8`).
    returns: stream object for reading/writing
    """
    try:
        from io import open as _open
    except ImportError:
        def _open(path, mode=None, encoding=None, **kwargs):
            return codecs.open(path, mode, encoding=encoding, **kwargs)
    return _open(path, mode=mode, encoding=encoding, **kwargs)


def get_file_contents(path, mode=None, encoding=None, **kwargs):
    """
    Load text file from file system and return content as text.
    * this function reads the entire content of the file before
      returning the data as a string or as bytes.

    :param path: path of file to read.
    :param mode: "b" for bytes or "t" for text (default is "t")
    :param encoding: file encoding for text (default is `utf-8`).
    :returns: file content as string or `None` if file cannot be read.
    """
    try:
        assert path is not None and os.path.isfile(path)
    except AssertionError:
        data = None
    else:
        if not mode:
            mode = ''
        mode = 'r%s' % mode
        if 'b' in mode:
            encoding = None
        else:
            # read file as text
            if not encoding:
                encoding = default_text_encoding
        with open_file(path, mode=mode, encoding=encoding, **kwargs) as file_obj:
            data = file_obj.read()
    return data


def write_file(path, data, mode=None, encoding=None, **kwargs):
    """
    Write text file to file system.

    :param path: path of file to write to.
    :param data: data to write.
    :param mode: "b" for bytes or "t" for text (default is "t")
    :param encoding: file encoding for text (default is `utf-8`).
    :returns: `True` if no error or `False` if ``IOError``.
    """
    if not mode:
        mode = ''
    mode = 'w%s' % mode
    if 'b' in mode:
        encoding = None
    else:
        if not encoding:
            encoding = default_text_encoding
    try:
        with open_file(path, mode=mode, encoding=encoding, **kwargs) as file_obj:
            file_obj.write(data)
        return True
    except IOError:
        return False


def delete_file(path):
    """
    Truncates file to zero size and
    tries to unlink file if possible.

    :param path: file system path for file
    :returns: True if file is unlinked (no longer found) else False
    """
    with open_file(path, mode='wb') as file_obj:
        file_obj.truncate(0)
    try:
        os.unlink(path)
    except OSError:
        pass
    return os.path.isfile(path) is False


# convert uri request string to list

PATH_SEP = '/'

def uri_to_list(path, path_sep=PATH_SEP):
    """
    Parse request path and split uri into list.

    * ``/action/param1/param2`` will be parsed as::

        ['action', 'param1', 'param2']

    * does not handle query strings

    :param path: uri (minus scheme and domain)
    :param path_sep: path separator (default is /)
    :returns: list of path components
    """
    try:
        if path[0] == path_sep:
            path = path[1:]
        if path[-1:] == path_sep:
            path = path[:-1]
    except IndexError:
        pass
    return path.split('/')


# data object class for storing generic dict key/value pairs
# * based on the Storage class from web.py
#
# class Storage(dict):
#   """
#   A Storage object is like a dictionary except `obj.foo` can be used
#   in addition to `obj['foo']`.
#
#       >>> o = storage(a=1)
#       >>> o.a
#       1
#       >>> o['a']
#       1
#       >>> o.a = 2
#       >>> o['a']
#       2
#       >>> del o.a
#       >>> o.a
#       Traceback (most recent call last):
#           ...
#       AttributeError: 'a'
#
#   """
#   def __getattr__(self, key):
#       try:
#           return self[key]
#       except KeyError, k:
#           raise AttributeError, k
#
#   def __setattr__(self, key, value):
#       self[key] = value
#
#   def __delattr__(self, key):
#       try:
#           del self[key]
#       except KeyError, k:
#           raise AttributeError, k
#
#   def __repr__(self):
#       return '<Storage ' + dict.__repr__(self) + '>'
#

class DataObject(dict):
    """
    Data object class.

    * based on ``webpy`` dict-like Storage object
    """
    def __init__(self, *args, **kwargs):
        self.add(*args, **kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError, k

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k

    def __repr__(self):
        return '<DataObject ' + dict.__repr__(self) + '>'

    def add(self, *args, **kwargs):
        """
        add({
            'a': 1,
            'b': 3.14,
            'c': 'foo'
        })
        """
        def add_dict(d):
            for name, value in d.items():
                self[name] = value
        add_dict(kwargs)
        for d in args:
            if isinstance(d, (list, tuple)):
                try:
                    for name in d:
                        self[name] = True
                except TypeError:
                    pass
            elif isinstance(d, dict):
                add_dict(d)
            else:
                self[d] = True


# class for configuration storage and management

class Config(object):
    """
    Class for storing configuration settings.
    """
    def __init__(self):
        """
        `namespaces` is list of namespaces defined.
        `config` is DataObject dict for configurations.
        `adhoc_namespace` is name of namespace to add vars to
        when no namespaces are specified in the ``set`` methods.
        """
        self.namespaces = []
        self.config = DataObject()
        self.adhoc_namespace = None

    def add_namespace(self, namespace, data={}):
        """Add a namespace or update an existing one with data."""
        if namespace not in self.namespaces:
            self.namespaces.insert(0, namespace)
            config = DataObject()
            self.config[namespace] = config
        else:
            config = self.get_namespace(namespace)
        if data:
            config.add(data)
        return config

    def get_namespace(self, namespace):
        """Return a config DataObject corresponding to `namespace`."""
        return self.config.get(namespace)

    def update_namespace(self, namespace, data):
        """
        Update the specified `namespace` with data.
        `data` should be dict.
        """
        if namespace in self.namespaces:
            self.config[namespace].add(data)
        else:
            raise AttributeError

    def delete_namespace(self, namespace):
        """Delete a namespace."""
        if namespace in self.namespaces:
            self.namespaces.remove(namespace)
            del self.config[namespace]

    def set_adhoc_namespace(self, namespace):
        """Set the `adhoc_namespace`."""
        self.adhoc_namespace = namespace
        if not namespace in self.namespaces:
            self.add_namespace(namespace)

    def setvar(self, namespace, key, val):
        """Set a var into the specified namespace."""
        try:
            config = self.config[namespace]
            config[key] = val
        except KeyError:
            raise KeyError(namespace)
        return val

    def getvar(self, namespace, key, default_val=None):
        """Get a var from the specified namespace."""
        try:
            config = self.config[namespace]
            return config.get(key, default_val)
        except KeyError:
            raise KeyError(namespace)

    def set(self, key, val, namespace=None):
        """
        Set a var -- if namespace is specified, key-value will be
        added to the namespace, otherwise the config object will
        try to insert it into the `adhoc_namespace` if defined.
        If `adhoc_namespace` is not set, the config object will
        raise a KeyError.
        """
        if not namespace:
            try:
                assert self.adhoc_namespace is not None
                return self.setvar(self.adhoc_namespace, key, val)
            except AssertionError:
                raise KeyError('No ad hoc namespace for setting value.')
        else:
            return self.setvar(namespace, key, val)

    def get(self, key, default_val=None, namespace=None):
        """
        Get a var -- if `namespace` is not specified, the
        config object will loop through the available namespaces
        and return the first match. If no matches are found,
        `default_val` or None is returned. The config object
        will search through namespaces in reverse order of
        definition so the last namespace added is searched first.
        """
        if not namespace:
            for _namespace in self.namespaces:
                config = self.config[_namespace]
                if key in config:
                    return config[key]
        else:
            return self.getvar(namespace, key, default_val)
        return default_val

    def update(self, namespace, data):
        """This is a shorthand for the ``update_namespace`` method."""
        self.update_namespace(namespace, data)


# based on `safeunicode` and `safestr` from web.py

def safe_unicode(obj, encoding='utf-8'):
    r"""
    Converts any given object to unicode string.

        >>> safe_unicode('hello')
        u'hello'
        >>> safe_unicode('你好')
        u'\u4f60\u597d'
        >>> safe_unicode(2)
        u'2'
        >>> safe_unicode(True)
        u'True'
        >>> safe_unicode(u'more caf\xe9')
        u'more caf\xe9'
        >>> safe_unicode('Ivan Krstić')
        u'Ivan Krsti\u0107'
        >>> safe_unicode(b'\xe1\x88\xb4')
        u'\u1234'
        >>> safe_unicode('ሴ')
        u'\u1234'

    """
    if isinstance(obj, six.binary_type):
        return obj.decode(encoding)
    elif isinstance(obj, six.string_types):
        return obj
    elif type(obj) in [int, float, bool]:
        return unicode(obj)
    else:
        if hasattr(obj, '__unicode__'):
            return unicode(obj)
        else:
            return str(obj).decode(encoding)


def safe_str(obj, encoding='utf-8'):
    r"""
    Converts any given object to utf-8 encoded string.

        >>> safe_str('hello')
        'hello'
        >>> safe_str('你好')
        '\xe4\xbd\xa0\xe5\xa5\xbd'
        >>> safe_str('Ivan Krstić')
        'Ivan Krsti\xc4\x87'
        >>> safe_str(u'\xe9criture \u5beb\u4f5c')
        '\xc3\xa9criture \xe5\xaf\xab\xe4\xbd\x9c'
        >>> safe_str('ሴ')
        '\xe1\x88\xb4'
        >>> safe_str(2)
        '2'
        >>> safe_str(True)
        'True'

    """
    if isinstance(obj, six.binary_type):
        return obj
    elif isinstance(obj, (six.text_type, six.string_types)):
        return obj.encode('utf-8')
    elif hasattr(obj, '__iter__'): # iterator
        return six.moves.map(safe_str, obj)
    else:
        return str(obj)


# simple logger

log_levels = {
            'notset': logging.NOTSET,
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }

log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def create_log(logname, logfile=None, level='debug', format=log_fmt):
    """
    Create and return simple file logger.

    * level is keyword in `log_levels` (`notset`, `debug`, `info`, etc.)
    * format is format of log entry to output

    :More info: `<http://docs.python.org/library/logging.html>`_

    :param logname: name of log.
    :param logfile: path of log file.
    :param level: log level (see ``log_levels``).
    :param format: log entry format (default is ``log_fmt``).
    :returns: logger object.
    """
    log_level = log_levels.get(level)
    logger = logging.getLogger(logname)
    logger.setLevel(log_level)
    if logfile:
        handler = logging.FileHandler(logfile)
    else:
        handler = logging.StreamHandler()
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter(format))
    logger.addHandler(handler)
    return logger
