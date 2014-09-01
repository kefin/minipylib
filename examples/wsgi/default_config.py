# -*- coding: utf-8 -*-
"""
wsgi.default_config

Default settings for wsgi.serve module.
"""

from __future__ import (absolute_import, unicode_literals)


# default wsgi server parameters
# * to customize configurations for your local server, place settings
#   in local_config.py

SERVER_CONFIG = {

    # server name
    'server': 'wsgiserver',

    # address (host, port) to bind server to
    'bind_addr': ('127.0.0.1', 8080), # (host, port)

    # user/group to run server process as
    'server_group': 'nogroup',
    'server_user': 'nobody',

    # app_type should be one of: wsgi, django or None
    'app_type': 'wsgi',

    # app should point to an application entry point if app_type is
    #   "wsgi" (this is ignored for django deployment.
    'app': None,

}
