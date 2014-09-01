# -*- coding: utf-8 -*-
"""
minipylib.server

The **minipylib.server** module contains adaptor classes to run a wsgi
server.

This modules allows you to configure and test your wsgi backend to use
a number of different wsgi servers -- the Python built-in
simple_server, the CherryPy wsgiserver, uwsgi, Linden Lab's eventlet,
fapws3, gevent, and bjoern.

Included in the minipylib distribution is a copy of the threaded
wsgiserver from `CherryPy <http://www.cherrypy.org/>`_. The
*wsgiserver* is the default server for the *minipylib.server* module.

``server_registry`` is dict of available servers.

* Unimportable servers will not be entered into the registry.
* The default server is CherryPy's wsgiserver (included in
  backends/cherrypy_wsgiserver directory)

Supported servers:

* wsgiserver: CherryPy wsgiserver (included in minipylib)
* cherry: CherryPy wsgiserver from package
* fapws: fapws3
* simple_server: python built-in wsgiref.simple_server
* uwsgi: uwsgi
* eventlet: Linden Lab eventlet
* gevent: gevent
* bjoern: bjoern
* waitress: waitress

* created: 2009-09-11 kevin chan <kefin@makedostudio.com>
* updated: 2014-08-30 kchan
"""

from __future__ import (absolute_import, unicode_literals)

from minipylib.server.settings import DEFAULT_SERVER_CONFIG
from minipylib.server.server_config import ServerConfig
from minipylib.server.utils import change_uid_gid
from minipylib.server.apps import test_app, get_django_app
from minipylib.server.backends.base import get_server_instance

# load backend servers (to populate the Server class registry)
from minipylib.server.backends import (
    wsgiserver,
    bjoern_server,
    cherrypy_server,
    eventlet_server,
    fapws_server,
    gevent_server,
    simple_server,
    uwsgi_server,
    waitress_server,
)

from minipylib.server.exceptions import (
    ServerNotFoundError,
    ServerConfigError,
)

def make_server(**params):
    """
    Return a Server adaptor object according to supplied params.

    To run server, create a Python file like the following and execute
    it using the interpreter or through a startup daemon script:

        from minipylib.server import make_server

        server_name = 'wsgiserver'
        app = my_wsgi_app
        bind_addr = ('127.0.0.1', 8080)
        server = make_server(server=server_name,
                             bind_addr=bind_addr,
                             app=app)

        if __name__ == '__main__':
            server.run()

    """
    server_name = params.get('server')
    app = params.get('app')
    if not app:
        if params.get('app_type') == 'django':
            app = get_django_app(server_name)
        else:
            app = test_app
        params['app'] = app
    config = ServerConfig(**params)
    return get_server_instance(server_name, config)


def get_web_server(**params):
    return make_server(**params)


#######################################################################
# Webserver class to run server.
# * class interface to create web server for compatibility with old code.
#######################################################################

class Webserver(object):
    """
    Class to manage wsgi server for web application.

    Params should include keys in the default server params below::

        app
        server
        bind_addr
        host_name
        server_user
        server_group

    Default settings::

        DEFAULT_SERVER = 'wsgiserver'
        DEFAULT_SERVER_HOST = '127.0.0.1'
        DEFAULT_SERVER_PORT = 8080

        DEFAULT_SERVER_USER = 'nobody'
        DEFAULT_SERVER_GROUP = 'nobody'

    How to use

    * create a Python source file called index.py (or whatever you
      want to name it).

    * in your **index.py**, create an instance of Webserver and provide
      appropriate parameters for your setup::

        server = Webserver(
                app=wsgi_application,
                server=WSGI_SERVER,
                bind_addr=(WSGI_SERVER_HOST, WSGI_SERVER_PORT)
        )

    :note: wsgi_application is your wsgi application.

    * run server::

        if __name__=="__main__":
            server.run()

    * or use a starter up script to start a wsgi server that runs as a daemon.

    """
    def __init__(self, **params):
        # older invocation code uses 'wsgi_server' instead of 'server'
        # so we set 'server' here so get_server_config will use
        # the correct server.
        if not 'server' in params:
            params['server'] = params.get('wsgi_server')
        c = get_server_config(**params)
        self.server = get_server_instance(c.server, c)

    def run(self):
        self.server.run()

    def stop(self):
        self.server.stop()
