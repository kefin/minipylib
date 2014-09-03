# -*- coding: utf-8 -*-
"""
minipylib.server.backends.uwsgi_server

Define a wsgi server object based on uwsgi.

"""

# created: 2011-04-17 Kevin Chan <kefin@makedostudio.com>
# updated: 2014-08-30 kchan

from __future__ import (absolute_import, unicode_literals)

from minipylib.server.backends.base import Server


#######################################################################
# uwsgi
# info:
# * https://github.com/unbit/uwsgi
# * https://uwsgi-docs.readthedocs.org/en/latest/

#######################################################################

try:
    import uwsgi

    class UwsgiServer(Server):
        """
        :source: https://github.com/unbit/uwsgi

        * uswgi serves differently than the other wsgi servers. The
          uwsgi configuration file will set the module to load and the
          "application" entry point (inside the module). We don't need
          to do anything here since the Server instance is not used to
          run a daemon process.
        * All uswgi options are set in XML file loaded by uswgi when
          invoked as daemon so we don't have to do any configuration
          here.
        """
        name = 'uwsgi'

        def run(self):
            pass

except ImportError:
    pass
