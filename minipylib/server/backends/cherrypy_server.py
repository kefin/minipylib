# -*- coding: utf-8 -*-
"""
minipylib.server.backends.cherrypy_server

Define a wsgi server object based on CherryPy's wsgiserver.

TThis module requires cherrypy as an installed package.

"""

# created: 2011-04-17 Kevin Chan <kefin@makedostudio.com>
# updated: 2014-08-30 kchan

from __future__ import (absolute_import, unicode_literals)

from minipylib.server.backends.base import Server
from minipylib.server.settings import DEFAULT_SERVER_CONFIG


#######################################################################
# CherryPy wsgiserver
# info: http://www.cherrypy.org/
#######################################################################

# add the wsgiserver server from the installed cherrypy package

DEFAULT_THREADS = DEFAULT_SERVER_CONFIG.get('threads', 4)

try:
    from cherrypy import wsgiserver as cherry

    class CherryPyServer(Server):
        """
        CherryPy wsgiserver

        :source: http://www.cherrypy.org/
        """
        name = 'cherrypy'

        def run(self):
            self.server = cherry.CherryPyWSGIServer(
                                    self.config.bind_addr,
                                    self.config.app,
                                    server_name=self.config.host_name,
                                    numthreads=self.config.get('threads',
                                                               DEFAULT_THREADS))
            try:
                self.server.start()
            except KeyboardInterrupt:
                self.stop()

        def stop(self):
            self.server.stop()


except ImportError:
    pass
