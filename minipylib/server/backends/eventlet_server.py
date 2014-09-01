# -*- coding: utf-8 -*-
"""
minipylib.server.backends.eventlet_server

Define a wsgi server object based on Linden Lab's eventlet.

* created: 2011-04-17 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-30 kchan
"""

from __future__ import (absolute_import, unicode_literals)

from minipylib.server.backends.base import Server


#######################################################################
# Linden Lab eventlet
# info:
# * http://eventlet.net/
# * https://pypi.python.org/pypi/eventlet/0.15.1
#######################################################################

try:
    import eventlet

    class EventletServer(Server):
        """
        Linden Lab eventlet
        * Don't know if this package is still current and being
          updated.

        :source:
        http://eventlet.net/
        https://pypi.python.org/pypi/eventlet/0.15.1
        """
        name = 'eventlet'

        def run(self):
            eventlet.wsgi.server(eventlet.listen(self.config.bind_addr),
                                 self.config.app)

except ImportError:
    pass
