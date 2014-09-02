# -*- coding: utf-8 -*-
"""
minipylib.server.backends.base

Definitions for a Server adaptor class.

* created: 2011-04-17 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-09-02 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import six

from minipylib.utils import DataObject
from minipylib.server.settings import DEFAULT_SERVER_CONFIG
from minipylib.server.exceptions import (
    ServerNotFoundError,
    ServerConfigError
)


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
    default_config = DEFAULT_SERVER_CONFIG

    def __init__(self, config):
        """
        Methods can access server parameters (host, port, app, etc.)
        through the "config" dict.

        :param config: config is a dict of key-value pairs to
            configure server
        """
        from minipylib.server.utils import change_uid_gid
        self.config = DataObject()
        self.set_config(self.default_config)
        self.set_config(config)
        self.server_name = self.config.server
        self.server = None
        user = self.config.server_user
        group = self.config.server_group
        if user and group:
            change_uid_gid(user, group)

    def set_config(self, config):
        """
        Set attributes based on parameters.
        * NOTE: config is a dict (not keyword args).
        * self.config is a DataObject (dict with values that can be
          accessed as object attributes).

        :param config: dict
        """
        self.config.add(config)

    def run(self):
        """
        Runs wsgi server. Subclass should override.
        """
        raise ServerConfigError('Server subclass should override "run" method.')

    def stop(self):
        """
        Stops wsgi server. Not all wsgi servers have a stop method.
        To stop server running as daemon, send kill signal to script.
        """
        pass


def get_server_registry():
    """Return server registry."""
    return Server.registry

def get_server_list():
    return get_server_registry()


def get_server_instance(server_name, config):
    """
    Return Server instance corresponding to server_name.

    :param server_name: keyword name of wsgi server
    :param config: config is a dict of server settings
    :returns: Server instance populated with config or None if error
    """
    registry = get_server_registry()
    try:
        server_obj = registry[server_name](config)
    except KeyError:
        raise ServerNotFoundError(
            "Cannot find Server class for: %s" % server_name)
    return server_obj
