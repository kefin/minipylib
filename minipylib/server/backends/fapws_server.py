# -*- coding: utf-8 -*-
"""
minipylib.server.backends.fapws_server

Define a wsgi server object based on fapws3.

"""

# created: 2011-04-17 Kevin Chan <kefin@makedostudio.com>
# updated: 2014-09-02 kchan

from __future__ import (absolute_import, unicode_literals)

import sys

from minipylib.server.backends.base import Server


#######################################################################
# fapws3
# info: http://www.fapws.org/
#######################################################################

try:
    import fapws._evwsgi as evwsgi
    from fapws import base

    class FapwsServer(Server):
        """
        FAPWS3 (Fast Asynchronous Python Web Server)
        * This project loosks to have been dormant/abandoned since 2012.

        :source: http://www.fapws.org/
        :source: https://github.com/william-os4y/fapws3
        """
        name = 'fapws'

        def run(self):
            try:
                # since we don't use threads, internal checks are no more required
                sys.setcheckinterval=100000
                # fapws evwsgi.start() seems to ignore the port
                # if it's a number and requires it to be a string,
                # so we cast it here to get it to work correctly.
                host, port = self.config.bind_addr
                evwsgi.start(host, str(port))
                evwsgi.set_base_module(base)
                evwsgi.wsgi_cb(('', self.config.app))
                evwsgi.set_debug(0)
                evwsgi.run()
            except KeyboardInterrupt:
                self.stop()

except ImportError:
    pass
