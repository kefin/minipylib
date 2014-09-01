# -*- coding: utf-8 -*-
"""
minipylib

Minipylib is a small library of utility functions
for developing python web applications.

* created: 2010-07-31 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-29 kchan
"""

from __future__ import (absolute_import, unicode_literals)


__author__ = 'Kevin Chan <kefin@makedostudio.com>'
__version_info__ = (0, 2, 9)
__version__ = '.'.join(map(str, __version_info__))

__description__ = """Minipylib is a small library of utility functions
for developing python web applications."""

VERSION = __version_info__
DESCRIPTION = __description__
AUTHOR = __author__
AUTHORS = (__author__,)


def get_version(version=None):
    """
    Returns a PEP 440 version string (in the form of major.minor.micro).
    Http://legacy.python.org/dev/peps/pep-0440/
    """
    if version is None:
        version = __version_info__
    if isinstance(version, (list, tuple)):
        version = '.'.join(map(str, version))
    return version
