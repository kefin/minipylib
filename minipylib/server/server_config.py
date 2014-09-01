# -*- coding: utf-8 -*-
"""
minipylib.server.server_config

Definition and functions to manage wsgi server configurations.

* created: 2011-04-17 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-09-01 kchan
"""

from __future__ import (absolute_import, unicode_literals)

from minipylib.server.settings import DEFAULT_SERVER_CONFIG


class ServerConfig(object):
    """
    Generic object for storing server settings.
    """

    def __init__(self, *args, **kwargs):
        """
        Instantiate class and set attributes based on kwargs.
        * args is ignored.
        """
        self._set_config(DEFAULT_SERVER_CONFIG)
        self._set_config(kwargs)

    def _set_config(self, params):
        """
        Set attributes based on params.
        NOTE: params is a dict (not keyword args).

        :param params: dict
        """
        for k, v in params.items():
            setattr(self, k, v)


def get_server_config(**params):
    """
    Return a ServerConfig object with settings for a wsgi server.
    """
    return ServerConfig(**params)
