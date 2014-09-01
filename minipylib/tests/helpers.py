# -*- coding: utf-8 -*-
"""
tests.helpers

Utility functions for minipylib tests.

* created: 2014-08-28 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-09-01 kchan
"""

from __future__ import (absolute_import, unicode_literals, print_function)

import six
import os
import unittest


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
        return unicode(obj)
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
        return itertools.imap(safestr, obj)
    else:
        return str(obj)


# divider for test diagnostic printouts (used by msg())
DIVIDER = '# ----------------------------------------------------------------------'

def msg(label, txt, first=False, linebreak=False, divider=DIVIDER):
    """
    Print out debug message.
    """
    if first:
        print('\n%s' % divider)
    label = safe_unicode(label)
    txt = safe_unicode(txt)
    if not linebreak:
        print('# %-16s : %s' % (label, txt))
    else:
        print('# %-16s :\n%s' % (label, txt))


def module_exists(module_name):
    """
    Check if module is importable.

    :param module_name: name of module to import (basestring)
    :returns: True if importable else False
    """
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True


# set TEST_DEBUG to True to output diagnostics and messages in tests
TEST_DEBUG = os.environ.get('TEST_DEBUG') is not None


class SimpleTestCase(unittest.TestCase):
    """
    Test case based on Python unittest TestCase.
    """
    # verbose debug messages
    debug_msgs = TEST_DEBUG

    def _msg(self, *args, **kwargs):
        """
        Utility method to print out verbose test and debug messages.
        * print output only if `debug_msgs` attribute is set to True.
        """
        if self.debug_msgs:
            msg(*args, **kwargs)
