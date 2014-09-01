# -*- coding: utf-8 -*-
"""
tests.server.tests

Tests for minipylib.server

* created: 2014-08-29 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-29 kchan
"""

from __future__ import absolute_import, unicode_literals

from minipylib.tests.helpers import SimpleTestCase


class ServerTests(SimpleTestCase):

    def test_server_config(self):
        """
        Ensure ServerConfig class is defined.
        """
        from minipylib.server.server_config import ServerConfig
        self._msg('test', 'ServerConfig', first=True)
        server_config = ServerConfig()
        self.assertTrue(server_config and isinstance(server_config, object))
        server_name = 'simple_server'
        server_config.server = server_name
        self.assertEqual(getattr(server_config, 'server'), server_name)

    def test_get_server_config(self):
        """
        Ensure get_server_config function is working properly.
        """
        from minipylib.server.server_config import get_server_config
        self._msg('test', 'get_server_config', first=True)
        c = get_server_config()
        self.assertTrue(c.server is not None)
        self.assertTrue(c.bind_addr is not None)
        self.assertTrue(c.server_user is not None)
        self.assertTrue(c.server_group is not None)

        self._msg('server', c.server)
        self._msg('bind_addr', c.bind_addr)
        self._msg('host_name', c.host_name)
        self._msg('server_user', c.server_user)
        self._msg('server_group', c.server_group)
        self._msg('app', c.app)
        

    def test_get_web_server(self):
        """
        Ensure get_web_server function is working properly.
        """
        self._msg('test', 'get_web_server', first=True)
        self._msg('TODO', '')


    def test_get_django_app(self):
        """
        Ensure get_django_app function is working properly.
        """
        self._msg('test', 'get_django_app', first=True)
        self._msg('TODO', '')


    def test_change_uid_gid(self):
        """
        Ensure change_uid_gid function is working properly.
        """
        self._msg('test', 'change_uid_gid', first=True)
        self._msg('TODO', '')


    def test_get_uid_gid(self):
        """
        Ensure get_uid_gid function is working properly.
        """
        self._msg('test', 'get_uid_gid', first=True)
        self._msg('TODO', '')

