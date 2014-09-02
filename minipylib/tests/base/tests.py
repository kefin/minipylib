# -*- coding: utf-8 -*-
"""
tests.base.tests

Base tests for minipylib.

* created: 2014-08-28 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-09-02 kchan
"""

from __future__ import (absolute_import, unicode_literals, print_function)

from minipylib.tests.helpers import (
    SimpleTestCase,
    module_exists,
)


class BaseTests(SimpleTestCase):

    def test_module_imports(self):
        """
        Ensure modules are importable.
        """
        apps = (
            'minipylib',
            'minipylib.crypto',
            'minipylib.utils',
            'minipylib.server',
            'minipylib.server.apps',
            'minipylib.server.settings',
            'minipylib.server.exceptions',
            'minipylib.server.utils',
            'minipylib.server.backends',
            'minipylib.server.backends.base',
            'minipylib.server.backends.bjoern_server',
            'minipylib.server.backends.cherrypy_server',
            'minipylib.server.backends.eventlet_server',
            'minipylib.server.backends.fapws_server',
            'minipylib.server.backends.gevent_server',
            'minipylib.server.backends.simple_server',
            'minipylib.server.backends.uwsgi_server',
            'minipylib.server.backends.wsgiserver',
            'minipylib.server.backends.waitress_server',
        )
        self._msg('test', 'module imports', first=True)
        for a in apps:
            exists = module_exists(a)
            self._msg('exists', '%s: %s' % (a, exists))
            self.assertTrue(module_exists(a),
                            msg='Cannot import module: %s' % a)

    def test_package_metadata(self):
        """
        Ensure version strings amd info are there.
        """
        self._msg('test', 'version', first=True)

        import minipylib
        version = minipylib.__version__
        version_string = minipylib.get_version()
        version_info = minipylib.VERSION
        version_string2 = minipylib.get_version(version_info)
        self.assertEqual(version_string2, version)
        self._msg('__version__', version)
        self._msg('get_version()', version_string)
        self._msg('VERSION', version_info)
        self._msg('get_version(VERSION)', version_string2)

        author = minipylib.__author__
        self.assertTrue(author)

        author_string = minipylib.AUTHOR
        self.assertEqual(author, author_string)

        authors = minipylib.AUTHORS
        self.assertTrue(len(authors) > 0)
        self.assertEqual(authors[0], author)

        self._msg('__author__', author)
        self._msg('AUTHOR', author_string)
        self._msg('AUTHORS', authors)

    def test_version(self):
        """
        Ensure get_version function is working.
        """
        self._msg('test', 'get_version()', first=True)
        import minipylib
        version = (1, 0, 1)
        version_string = "1.0.1"
        result = minipylib.get_version(version)
        self.assertEqual(result, version_string)
        self._msg('version', version)
        self._msg('expected', version_string)
        self._msg('result', result)

        version = (0, 0, 12)
        version_string = "1.0.1"
        result = minipylib.get_version(version)
        self.assertNotEqual(result, version_string)
        self._msg('version', version)
        self._msg('result', result)

        version = (0, 0, "a")
        version_string = "0.0.a"
        result = minipylib.get_version(version)
        self.assertEqual(result, version_string)
        self._msg('version', version)
        self._msg('expected', version_string)
        self._msg('result', result)
