# -*- coding: utf-8 -*-
"""
minipylib.server.backends.simple_server

Define a wsgi server object based on the Python simple_server.

"""

# created: 2011-04-17 Kevin Chan <kefin@makedostudio.com>
# updated: 2014-08-30 kchan

from __future__ import (absolute_import, unicode_literals)

from minipylib.server.backends.base import Server


#######################################################################
# wsgiref.simple_server
# * python bulit-in wsgiref.simple_server (only available in
#   Python 2.5 or above).
#######################################################################

try:
    from wsgiref.simple_server import make_server as _make_server

    class SimpleServer(Server):
        """
        Python bulit-in ``wsgiref.simple_server``.
        """
        name = 'simple_server'

        def run(self):
            host, port = self.config.bind_addr
            self.server = _make_server(host, port, self.config.app)
            try:
                self.server.serve_forever()
            except KeyboardInterrupt:
                self.stop()

except ImportError:
    pass
