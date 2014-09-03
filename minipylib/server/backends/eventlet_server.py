# -*- coding: utf-8 -*-
"""
minipylib.server.backends.eventlet_server

Define a wsgi server object based on Linden Lab's eventlet.

"""

# created: 2011-04-17 Kevin Chan <kefin@makedostudio.com>
# updated: 2014-09-02 kchan

from __future__ import (absolute_import, unicode_literals)

from minipylib.server.backends.base import Server


#######################################################################
# Linden Lab eventlet
# info:
# * http://eventlet.net/
# * https://bitbucket.org/eventlet/eventlet
# * https://github.com/eventlet/eventlet/
#######################################################################

try:
    from eventlet.wsgi import server as eventlet_server
    from eventlet import listen as socket_listener

    class EventletServer(Server):
        """
        Linden Lab eventlet

        Eventlet is a concurrent networking library for Python that
        allows you to change how you run your code, not how you write
        it.

        It uses epoll or libevent for highly scalable non-blocking
        I/O. Coroutines ensure that the developer uses a blocking
        style of programming that is similar to threading, but provide
        the benefits of non-blocking I/O. The event dispatch is
        implicit, which means you can easily use Eventlet from the
        Python interpreter, or as a small part of a larger
        application.

        :source:
        http://eventlet.net/
        https://bitbucket.org/eventlet/eventlet
        https://github.com/eventlet/eventlet/
        """
        name = 'eventlet'

        def run(self):
            server_socket = socket_listener(self.config.bind_addr)
            eventlet_server(server_socket, self.config.app)

except ImportError:
    pass
