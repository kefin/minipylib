# -*- coding: utf-8 -*-
"""
minipylib.server.backends.wsgiserver

Define a wsgi server object based on a local copy of CherryPy's wsgiserver.

* created: 2011-04-17 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-30 kchan
"""

from __future__ import (absolute_import, unicode_literals)

from minipylib.server.backends.base import Server
from minipylib.server.settings import DEFAULT_SERVER_CONFIG


#######################################################################
# local copy of CherryPy wsgiserver (included in minipylib)
#######################################################################

DEFAULT_THREADS = DEFAULT_SERVER_CONFIG.get('threads', 4)

try:
    from . import cherrypy_wsgiserver as wsgiserver

    class WsgiServer(Server):
        """
        CherryPy wsgiserver

        * This module is copied from the Cherrypy distribution.
        """
        name = 'wsgiserver'

        def run(self):
            self.server = wsgiserver.CherryPyWSGIServer(
                                        self.config.bind_addr,
                                        self.config.app,
                                        server_name=self.config.host_name,
                                        numthreads=getattr(self.config,
                                                           'threads',
                                                           DEFAULT_THREADS))
            try:
                self.server.start()
            except KeyboardInterrupt:
                self.stop()

        def stop(self):
            self.server.stop()

except ImportError:
    pass
