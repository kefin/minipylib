# -*- coding: utf-8 -*-
"""
minipylib.server.backends.waitress_server

Define a wsgi server object based on waitress.

* created: 2014-08-30 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-30 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import sys

from minipylib.server.backends.base import Server


try:
    import waitress

    class WaitressServer(Server):
        """
        Waitress server.

        Waitress is meant to be a production-quality pure-Python WSGI
        server with very acceptable performance. It has no
        dependencies except ones which live in the Python standard
        library. It runs on CPython on Unix and Windows under Python
        2.6+ and Python 3.2+. It is also known to run on PyPy 1.6.0 on
        UNIX. It supports HTTP/1.0 and HTTP/1.1.
        
        :source: https://waitress.readthedocs.org/
        """
        name = 'waitress'

        def run(self):
            host, port = self.config.bind_addr
            try:
                waitress.serve(self.config.app, host=host, port=port)
            except KeyboardInterrupt:
                self.stop()

except ImportError:
    pass
