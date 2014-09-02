# -*- coding: utf-8 -*-
"""
minipylib.server.backends.gevent_server

Define a wsgi server object based on gevent.

* created: 2011-04-17 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-30 kchan
"""

from __future__ import (absolute_import, unicode_literals)

from minipylib.server.backends.base import Server


#######################################################################
# gevent pywsgi server
# info:
# * http://www.gevent.org/
# * https://github.com/surfly/gevent
#######################################################################

try:
    from gevent.pywsgi import WSGIServer as gevent_pywsgi

    class GeventPYWsgiServer(Server):
        """
        gevent.pywsgi.WSGIServer

        :source:
        http://www.gevent.org/
        https://github.com/surfly/gevent
        """
        name = 'gevent'

        def run(self):
            self.server = gevent_pywsgi(self.config.bind_addr,
                                        self.config.app)
            self.server.serve_forever()

except ImportError:
    pass
