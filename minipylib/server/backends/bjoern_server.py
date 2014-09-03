# -*- coding: utf-8 -*-
"""
minipylib.server.backends.bjoern_server

Define a wsgi server object based on bjoern.

"""

# created: 2011-04-17 Kevin Chan <kefin@makedostudio.com>
# updated: 2014-08-30 kchan

from __future__ import (absolute_import, unicode_literals)

from minipylib.server.backends.base import Server


#######################################################################
# bjoern server
# info: https://github.com/jonashaag/bjoern
#######################################################################

try:
    import bjoern

    class BjoernServer(Server):
        """
        bjoern

        :source: https://github.com/jonashaag/bjoern
        """
        name = 'bjoern'

        def run(self):
            host, port = self.config.bind_addr
            bjoern.listen(self.config.app, host, port)
            bjoern.run()

except ImportError:
    pass
