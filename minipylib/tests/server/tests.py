# -*- coding: utf-8 -*-
"""
tests.server.tests

Tests for minipylib.server

* created: 2014-08-29 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-09-01 kchan
"""

from __future__ import absolute_import, unicode_literals

from mock import Mock, patch, call

from minipylib.tests.helpers import SimpleTestCase


TEST_SERVER_CONFIG = {

    # server name
    'server': 'fapws',

    # address (host, port) to bind server to
    'bind_addr': ('127.0.0.1', 8085),
    'host_name': 'example.com',

    # user/group to run server process as
    'server_user': 'server',
    'server_group': 'admin',

    # app_type should be one of: wsgi, django or None
    'app_type': 'django', # wsgi, django or None

    # app should point to an application entry point if app_type is
    #   "wsgi" (this is ignored for django deployment.
    'app': None,

    # number of threads for servers that use them (like cherrypy):
    'threads': 10,
}

class ServerTests(SimpleTestCase):

    def test_default_server_config(self):
        """
        Ensure DEFAULT_SERVER_CONFIG is defined correctly.
        """
        from minipylib.server.settings import DEFAULT_SERVER_CONFIG as _conf
        self._msg('test', 'DEFAULT_SERVER_CONFIG', first=True)
        settings = [
            'server', 'bind_addr', 'host_name', 'server_user', 'server_group',
            'app_type', 'app', 'threads'
        ]
        # verify settings exist in DEFAULT_SERVER_CONFIG
        for s in settings:
            self.assertTrue(s in _conf,
                            msg='key not found: %s' % s)
            self._msg(s, _conf.get(s))
        # check default bind address
        self.assertTrue(isinstance(_conf.get('bind_addr'), (list, tuple)))


    def test_server_config(self):
        """
        Ensure ServerConfig class is defined.
        """
        from minipylib.server.server_config import ServerConfig
        self._msg('test', 'ServerConfig', first=True)
        my_config = {}
        my_config.update(TEST_SERVER_CONFIG)
        self._msg('my_config', my_config)
        c = ServerConfig(**my_config)
        self.assertTrue(c and isinstance(c, object))
        for k, v in my_config.items():
            cval = getattr(c, k)
            self.assertEqual(cval, v)
            self._msg(k, cval)

    def test_get_server_config(self):
        """
        Ensure get_server_config function is working properly.
        """
        from minipylib.server.server_config import get_server_config
        self._msg('test', 'get_server_config', first=True)

        c = get_server_config()
        self._msg('config', c)
        self.assertTrue(c.server is not None)
        self.assertTrue(c.bind_addr is not None)
        self.assertTrue(c.server_user is not None)
        self.assertTrue(c.server_group is not None)

        self._msg('server', c.server)
        self._msg('bind_addr', c.bind_addr)
        self._msg('host_name', c.host_name)
        self._msg('server_user', c.server_user)
        self._msg('server_group', c.server_group)
        self._msg('app_type', c.app_type)
        self._msg('app', c.app)

        self._msg('***', '')
        my_config = {}
        my_config.update(TEST_SERVER_CONFIG)
        self._msg('my_config', my_config)
        c = get_server_config(**my_config)
        self.assertTrue(c and isinstance(c, object))
        self._msg('config', c)
        for k, v in my_config.items():
            cval = getattr(c, k)
            self.assertEqual(cval, v)
            self._msg(k, cval)

    def test_make_server(self):
        """
        Ensure make_server function is working properly.
        """
        from minipylib.server import make_server
        self._msg('test', 'make_server', first=True)
        my_config = {}
        my_config.update(TEST_SERVER_CONFIG)
        s = make_server(**my_config)
        self.assertTrue(s and isinstance(s, object))
        self.assertTrue(callable(s.run))
        for k, v in my_config.items():
            cval = getattr(s.config, k)
            if k != 'app':
                self.assertEqual(cval, v)
            else:
                self.assertTrue(callable(cval))
            self._msg(k, cval)

    def test_get_web_server(self):
        """
        Ensure get_web_server function is working properly.
        """
        from minipylib.server import get_web_server
        self._msg('test', 'get_web_server', first=True)
        my_config = {}
        my_config.update(TEST_SERVER_CONFIG)
        s = get_web_server(**my_config)
        self.assertTrue(s and isinstance(s, object))
        self.assertTrue(callable(s.run))
        for k, v in TEST_SERVER_CONFIG.items():
            cval = getattr(s.config, k)
            if k != 'app':
                self.assertEqual(cval, v)
            else:
                self.assertTrue(callable(cval))
            self._msg(k, cval)

    def test_get_django_app(self):
        """
        Ensure get_django_app function is working properly.
        """
        from minipylib.server import get_django_app
        self._msg('test', 'get_django_app', first=True)
        server = 'uwsgi'
        app = get_django_app(server)
        self.assertTrue(callable(app))
        self._msg('django app', app)

    @patch('grp.getgrnam')
    @patch('pwd.getpwnam')
    def test_get_uid_gid(self, mock_getpwnam, mock_getgrnam):
        """
        Ensure get_uid_gid function is working properly.
        """
        from minipylib.server import get_uid_gid
        self._msg('test', 'get_uid_gid', first=True)

        # test root/root
        pw_name = 'root'
        pw_passwd = 'x'
        pw_uid = 0
        pw_gid = 0
        pw_gecos = ''
        pw_dir = '/root'
        pw_shell = '/bin/sh'
        mock_getpwnam.return_value = (pw_name, pw_passwd, pw_uid, pw_gid,
                                      pw_gecos, pw_dir, pw_shell)
        gr_name = 'root'
        gr_passwd = 'x'
        gr_gid = 0
        gr_mem = 'root'
        mock_getgrnam.return_value = (gr_name, gr_passwd, gr_gid, gr_mem)

        user = 'root'
        group = 'root'
        uid, gid = get_uid_gid(user, group)
        pwd_call_args = mock_getpwnam.call_args
        grp_call_args = mock_getgrnam.call_args

        self.assertEqual(uid, pw_uid,
                         msg='uid should be %d (got %d)' % (pw_uid, uid))
        self.assertEqual(gid, gr_gid,
                         msg='gid should be %s (got %d)' % (gr_gid, gid))
        self.assertEqual(pwd_call_args, call(pw_name))
        self.assertEqual(grp_call_args, call(gr_name))
        self._msg(user, uid)
        self._msg(group, gid)
        self._msg('pwd_call_args', pwd_call_args)
        self._msg('grp_call_args', grp_call_args)

        # test nobody/nogroup
        pw_name = 'nobody'
        pw_passwd = 'x'
        pw_uid = 12345678
        pw_gid = 98765432
        pw_gecos = ''
        pw_dir = '/nonexistent'
        pw_shell = '/usr/sbin/nologin'
        mock_getpwnam.return_value = (pw_name, pw_passwd, pw_uid, pw_gid,
                                      pw_gecos, pw_dir, pw_shell)

        gr_name = 'nogroup'
        gr_passwd = 'x'
        gr_gid = 98765432
        gr_mem = 'nobody'
        mock_getgrnam.return_value = (gr_name, gr_passwd, gr_gid, gr_mem)

        user = 'nobody'
        group = 'nogroup'
        uid, gid = get_uid_gid(user, group)
        pwd_call_args = mock_getpwnam.call_args
        grp_call_args = mock_getgrnam.call_args

        self.assertEqual(uid, pw_uid,
                         msg='uid should be %d (got %d)' % (pw_uid, uid))
        self.assertEqual(gid, gr_gid,
                         msg='gid should be %s (got %d)' % (gr_gid, gid))
        self.assertEqual(pwd_call_args, call(pw_name))
        self.assertEqual(grp_call_args, call(gr_name))
        self._msg(user, uid)
        self._msg(group, gid)
        self._msg('pwd_call_args', pwd_call_args)
        self._msg('grp_call_args', grp_call_args)

    @patch('os.setgid')
    @patch('os.setuid')
    @patch('minipylib.server.utils.get_uid_gid')
    @patch('os.geteuid')
    def test_change_uid_gid(self, mock_geteuid, mock_get_uid_gid,
                            mock_setuid, mock_setgid):
        """
        Ensure change_uid_gid function is working properly.
        """
        from minipylib.server import change_uid_gid
        self._msg('test', 'change_uid_gid', first=True)

        user = 'nobody'
        group = 'nogroup'
        uid = 12345678
        gid = 98765432

        mock_get_uid_gid.return_value = (uid, gid)
        mock_geteuid.return_value = -1
        change_uid_gid(user, group)
        self.assertFalse(mock_setgid.called)
        self.assertFalse(mock_setuid.called)

        mock_get_uid_gid.return_value = (uid, gid)
        mock_geteuid.return_value = 0
        change_uid_gid(user, group)
        self.assertTrue(mock_setgid.called)
        self.assertTrue(mock_setuid.called)

        get_uid_gid_call_args = mock_get_uid_gid.call_args
        setgid_call_args = mock_setgid.call_args
        setuid_call_args = mock_setuid.call_args
        self.assertEqual(get_uid_gid_call_args, call(user, group))
        self.assertEqual(setgid_call_args, call(gid))
        self.assertEqual(setuid_call_args, call(uid))
        self._msg('get_uid_gid_call_args', get_uid_gid_call_args)
        self._msg('setgid_call_args', setgid_call_args)
        self._msg('setuid_call_args', setuid_call_args)

    def test_get_server_registry(self):
        """
        Ensure get_server_registry function is working properly.
        """
        from minipylib.server.backends.base import get_server_registry
        self._msg('test', 'get_server_registry')
        registry = get_server_registry()
        # should have at least one server definition (wsgiserver)
        self.assertTrue(len(registry) > 0)
        self.assertTrue(registry.get('wsgiserver'))
        for server_name, server_cls in registry.items():
            self.assertTrue(isinstance(server_cls, object))
            self.assertTrue(hasattr(server_cls, 'run'))
            self.assertTrue(hasattr(server_cls, 'stop'))
            self.assertTrue(callable(server_cls.run))
            self._msg(server_name, server_cls)

    def test_get_server_list(self):
        """
        Ensure get_server_list function is working properly.
        """
        from minipylib.server.backends.base import (
            get_server_registry,
            get_server_list
        )
        self._msg('test', 'get_server_list')
        registry1 = get_server_list()
        registry2 = get_server_registry()
        self.assertEqual(registry1, registry2)
        self._msg('registry', registry1)

    def test_server_object(self):
        """
        Ensure Server object is working correctly.
        """
        from minipylib.server.server_config import get_server_config
        from minipylib.server.backends.base import (
            Server,
            get_server_registry
        )
        self._msg('test', 'Server object', first=True)

        server_name = 'dummy-test-server'

        class TestServer(Server):
            name = server_name
            def run(self):
                pass

        registry = get_server_registry()
        dummy_server_cls = registry.get(server_name)
        self.assertTrue(dummy_server_cls is not None)

        my_config = {}
        my_config.update(TEST_SERVER_CONFIG)
        config = get_server_config(**my_config)

        dummy_server = dummy_server_cls(config)
        self.assertTrue(isinstance(dummy_server, object))
        self.assertTrue(isinstance(dummy_server, Server))
        self.assertTrue(isinstance(dummy_server, TestServer))

        self.assertEqual(dummy_server.name, server_name)
        self.assertTrue(callable(dummy_server.run))
        self._msg('server name', server_name)
        self._msg('dummy server', dummy_server)

        self.assertTrue(dummy_server.config is not None)
        for k, v in my_config.items():
            cval = getattr(dummy_server.config, k)
            self.assertEqual(cval, v)
            self._msg(k, cval)


    def test_get_server_instance(self):
        """
        Ensure get_server_instance function is working properly.
        """
        from minipylib.server.server_config import get_server_config
        from minipylib.server.backends.base import (
            Server,
            get_server_registry,
            get_server_instance
        )
        self._msg('test', 'get_server_instance', first=True)

        server_name = 'dummy-test-server'

        class TestServer(Server):
            name = server_name
            def run(self):
                pass

        registry = get_server_registry()
        dummy_server_cls = registry.get(server_name)
        self.assertTrue(dummy_server_cls is not None)

        my_config = {}
        my_config.update(TEST_SERVER_CONFIG)
        config = get_server_config(**my_config)

        dummy_server1 = dummy_server_cls(config)
        self.assertTrue(isinstance(dummy_server1, object))
        self.assertTrue(isinstance(dummy_server1, Server))
        self.assertTrue(isinstance(dummy_server1, TestServer))

        dummy_server2 = get_server_instance(server_name, config)
        self.assertTrue(isinstance(dummy_server2, object))
        self.assertTrue(isinstance(dummy_server2, Server))
        self.assertTrue(isinstance(dummy_server2, TestServer))
        self.assertTrue(callable(dummy_server2.run))
        self._msg('server name', server_name)
        self._msg('dummy server 1', dummy_server1)
        self._msg('dummy server 2', dummy_server2)

        self.assertTrue(dummy_server2.config is not None)
        for k, v in my_config.items():
            cval = getattr(dummy_server2.config, k)
            self.assertEqual(cval, v)
            self._msg(k, cval)


    def test_make_server(self):
        """
        Ensure make_server function is working properly.
        """
        self._msg('test', 'make_server', first=True)
        self._msg('TODO')
