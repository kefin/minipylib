# -*- coding: utf-8 -*-
"""
wsgi.serve

Glue code for running wsgi server and web application.

This module uses minipylib.server to create a wsgi server to load a
wsgi web application. When run as a standalone Python script this file
will create an instance of the wsgi server and run it as a daemon
process (except when using the uwsgi server, which can run itself in
daemon mode).

See doc string for `create_server` for details on parameters.

Servers with built-in adaptors in minipylib.server module:

* wsgiserver: CherryPy wsgiserver (included in minipy)
* cherrypy: CherryPy wsgiserver from package
* fapws: fapws3
* simple_server: python built-in wsgiref.simple_server
* uwsgi: uwsgi
* eventlet: Linden Lab eventlet
* gevent: gevent
* bjoern: bjoern
* waitress: waitress

* created: 2013-10-29 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-30 kchan
"""

from __future__ import (absolute_import, unicode_literals)

from minipylib.server import make_server

# load configurations
try:
    from wsgi.local_config import SERVER_CONFIG
except ImportError:
    from wsgi.default_config import SERVER_CONFIG


_server = make_server(**SERVER_CONFIG)

# needed for uwsgi to call application entry point
application = _server.config.app


if __name__ == "__main__":
    # start server and run as daemon
    # * this file is exceuted as a standalone Python script running
    #   a wsgi server daemon process.
    # * note: uwsgi works differently and runs in daemon mode, so
    #   __main__ is never called. Instead, it will call the callable
    #   assigned to "application" (see the "application" var above).
    _server.run()
