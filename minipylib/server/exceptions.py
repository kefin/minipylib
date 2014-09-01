# -*- coding: utf-8 -*-
"""
minipylib.server.exceptions

Exceptions for minipylib.server module.

* created: 2014-08-30 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-09-01 kchan
"""

from __future__ import (absolute_import, unicode_literals)


class ServerNotFoundError(Exception):
    """Raised when a server is not found in the server registry."""
    pass


class ServerConfigError(Exception):
    """Raised when server contains configuration errors."""
    pass
