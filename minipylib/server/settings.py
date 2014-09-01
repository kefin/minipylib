# -*- coding: utf-8 -*-
"""
minipylib.server.settings

Default settings for the server module.

* created: 2011-04-17 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-29 kchan
"""

from __future__ import unicode_literals


DEFAULT_SERVER_CONFIG = {

    # server name
    'server': 'wsgiserver',

    # address (host, port) to bind server to
    'bind_addr': ('127.0.0.1', 8080),
    'host_name': '',
    
    # user/group to run server process as
    'server_user': 'nobody',
    'server_group': 'nogroup',

    # app_type should be one of: wsgi, django or None
    'app_type': 'wsgi', # wsgi, django or None

    # app should point to an application entry point if app_type is
    #   "wsgi" (this is ignored for django deployment.
    'app': None,

    # number of threads for servers that use them (like cherrypy):
    'threads': 10,
}
