# -*- coding: utf-8 -*-
"""
minipylib.server.backends.base

Definitions for a Server adaptor class.

* created: 2011-04-17 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-30 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import six


class ServerMeta(type):
    """
    Metaclass with registry attribute to keep track of subclasses.
    """
    def __init__(cls, name, bases, dct):
        if not hasattr(cls, 'registry'):
            # base class - create empty registry.
            cls.registry = {}
        else:
            if not hasattr(cls, 'name') or not cls.name:
                cls.name = name.lower()
            # derived class - add cls to registry.
            cls.registry[cls.name] = cls

        super(ServerMeta, cls).__init__(name, bases, dct)


@six.add_metaclass(ServerMeta)
class Server(object):
    """
    Template for wsgi server adaptor.
    * the Server class defines "run" and "stop" methods to start/stop
      a wsgi server running as a daemon.
    """

    name = None

    def __init__(self, config):
        """
        Methods can access server parameters (host, port, app, etc.)
        through the "config" dict.

        :param config: config is a ServerConfig object.
        """
        from minipylib.server.utils import change_uid_gid
        self.config = config
        self.server = config.server
        user = config.server_user
        group = config.server_group
        if user and group:
            change_uid_gid(user, group)

    def run(self):
        """
        Runs wsgi server. Subclass should override.
        """
        pass

    def stop(self):
        """
        Stops wsgi server. Not all wsgi servers have a stop method.
        To stop server running as daemon, send kill signal to script.
        """
        pass


def get_server_registry():
    """
    Return server registry.
    """
    return Server.registry

def get_server_list():
    return get_server_registry()


def get_server_instance(server, config):
    """
    Return Server instance corresponding to name.

    :param server: keyword name of wsgi server
    :param config: config is a ServerConfig object
    :returns: Server instance populated with config or None if error
    """
    from minipylib.server.exceptions import ServerNotFoundError
    registry = get_server_registry()
    try:
        server_obj = registry[server](config)
    except KeyError:
        raise ServerNotFoundError("Cannot find Server subclass: %s" % server)
    return server_obj
