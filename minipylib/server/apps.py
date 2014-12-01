# -*- coding: utf-8 -*-
"""
minipylib.server.apps

Wsgi app helper functions for the server module.

"""

# created: 2011-04-17 Kevin Chan <kefin@makedostudio.com>
# updated: 2014-09-30 kchan

from __future__ import (absolute_import, unicode_literals)


# test_app - generic test app for testing wsgi server

try:
    # this will only fail if we have an old version of Pythin (<2.5)
    # if sys.hexversion >= 0x2050000:
    from wsgiref.simple_server import demo_app
    test_app = demo_app
except ImportError:
    def test_app(environ, start_response):
        """
        Simplest possible application object
        * from PEP 333 - http://www.python.org/dev/peps/pep-0333/
        """
        status = '200 OK'
        response_headers = [('Content-type','text/plain')]
        start_response(status, response_headers)
        return [b'Hello world!\n']


# get_django_app - get app for serving a django project

def get_django_app(server):
    """
    Return wsgi app serving django project.

    `server` is server type:

    * fapws
    * wsgiserver
    * cherrypy
    * simple_server
    * uwsgi
    * eventlet
    * gevent
    * bjoern
    """
    try:
        import django
        #from django.core.handlers.wsgi import WSGIHandler
        from django.core.wsgi import get_wsgi_application
    except ImportError:
        class WSGIHandler(object):
            def __call__(self, environ, start_response):
                status = '200 OK'
                response_headers = [('Content-type','text/plain')]
                start_response(status, response_headers)
                return [b'Unable to import django. Please check your installation.\n']

    if server == 'fapws':
        # from fapws.contrib.django_handler
        def django_handler(environ, start_response):
            wsgi_handler = WSGIHandler()
            response = wsgi_handler(environ, start_response)
            try:
                if django.VERSION[0] == 0:
                    for key, val in response.headers.items():
                        start_response.response_headers[key] = val
                else:
                    for key, val in response._headers.values():
                        start_response.response_headers[key] = val
                start_response.cookies = response.cookies
                return [response.content]
            except (NameError, AttributeError):
                return response
        return django_handler
    else:
        return get_wsgi_application()
