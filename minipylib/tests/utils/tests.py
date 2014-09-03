# -*- coding: utf-8 -*-
"""
tests.utils.tests

Tests for minipylib.utils

* created: 2014-08-29 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-29 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import six
import os
import sys

from minipylib.tests.helpers import SimpleTestCase


TestData = """\
This is a test file.
"""

class UtilsTests(SimpleTestCase):

    def test_add_to_sys_path(self):
        """
        Ensure add_to_sys_path function is working properly.
        """
        from minipylib.utils import add_to_sys_path
        self._msg('test', 'add_to_sys_path', first=True)
        module_dir = os.path.dirname(os.path.realpath(__file__))
        in_sys_path = module_dir in sys.path
        self.assertFalse(in_sys_path)
        add_to_sys_path(module_dir)
        in_sys_path = module_dir in sys.path
        self.assertTrue(in_sys_path)
        self._msg('module_dir', module_dir)
        self._msg('in sys.path', in_sys_path)
        self._msg('sys.path', sys.path)


    def test_import_module(self):
        """
        Ensure import_module function is working properly.
        """
        from minipylib.utils import import_module
        self._msg('test', 'import_module', first=True)
        module_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(module_dir, 'dummy_module', 'settings.py')
        imported = import_module(path)
        admin_user = 'dummy-admin'
        max_length = 1000
        self._msg('path', path)
        self._msg('module', imported)
        self._msg('module_name', imported.__name__)
        self.assertEqual(imported.ADMIN_USER, admin_user)
        self.assertEqual(imported.MAX_LENGTH, max_length)
        self._msg('ADMIN_USER', imported.ADMIN_USER)
        self._msg('MAX_LENGTH', imported.MAX_LENGTH)


    def test_import_module_vars(self):
        """
        Ensure import_module_vars function is working properly.
        """
        from minipylib.utils import import_module_vars
        self._msg('test', 'import_module_vars', first=True)
        example_settings_module = 'minipylib.tests.utils.dummy_module.settings'
        dummy_settings = {
            'ADMIN_USER': 'dummy-admin',
            'MAX_LENGTH': 1000
        }
        varnames = dummy_settings.keys()
        example_settings = import_module_vars(example_settings_module,
                                              varnames=varnames)
        self.assertTrue(varnames)
        self._msg('example_settings_module', example_settings_module)
        for v in varnames:
            self.assertEqual(example_settings[v], dummy_settings[v])
            self._msg(v, example_settings[v])


    def test_import_module_settings(self):
        """
        Ensure import_module_settings function is working properly.
        """
        from minipylib.utils import import_module_settings
        self._msg('test', 'import_module_settings', first=True)
        example_settings_module = 'minipylib.tests.utils.dummy_module.settings'
        dummy_settings = {
            'ADMIN_USER': 'dummy-admin',
            'MAX_LENGTH': 1000
        }
        varnames = dummy_settings.keys()
        example_settings = import_module_settings(example_settings_module)
        self.assertTrue(varnames)
        for v in varnames:
            self.assertEqual(example_settings[v], dummy_settings[v])
            self._msg(v, example_settings[v])


    def test_get_instance(self):
        """
        Ensure get_instance function is working properly.
        """
        from minipylib.utils import get_instance
        self._msg('test', 'get_instance', first=True)
        dummy_module = 'minipylib.tests.utils.dummy_module.objects'
        class_name = 'DummyTestObject'
        name = 'dummy-object'
        obj = get_instance(dummy_module, class_name, name)
        self.assertTrue(obj and isinstance(obj, object))
        self.assertEqual(obj.get_name(), name)
        self._msg('obj', obj)
        self._msg('name', obj.get_name())


    def test_get_file_contents(self):
        """
        Ensure get_file_contents function is working properly.
        """
        from minipylib.utils import get_file_contents
        self._msg('test', 'get_file_contents', first=True)
        module_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(module_dir, 'testfile.txt')
        data = get_file_contents(path)
        self._msg('path', path)
        self._msg('data', data, linebreak=True)
        self.assertEqual(data, TestData)

        path = os.path.join(module_dir, 'no_such_file')
        data = get_file_contents(path)
        self._msg('path', path)
        self._msg('data', data)
        self.assertTrue(data is None)

        path = os.path.join(module_dir, 'ico_loading.gif')
        data = get_file_contents(path, mode='b')
        self.assertTrue(isinstance(data, six.binary_type))
        self._msg('path', path)
        self._msg('data type', type(data))
        self._msg('data', repr(data), linebreak=True)


    def test_write_file(self):
        """
        Ensure write_file function is working properly.
        """
        import tempfile
        from minipylib.utils import write_file, get_file_contents
        self._msg('test', 'write_file', first=True)
        filename = 'minipylib-testfile'
        tmpfile_dir = tempfile.gettempdir()
        path = os.path.join(tmpfile_dir, filename)
        result = write_file(path, TestData)
        self.assertTrue(result)
        # check contents
        data = get_file_contents(path)
        self._msg('path', path)
        self._msg('data', data, linebreak=True)
        self.assertEqual(data, TestData)
        os.unlink(path)


    def test_delete_file(self):
        """
        Ensure delete_file function is working properly.
        """
        import tempfile
        from minipylib.utils import write_file, delete_file
        self._msg('test', 'delete_file', first=True)
        filename = 'minipylib-testfile'
        tmpfile_dir = tempfile.gettempdir()
        path = os.path.join(tmpfile_dir, filename)
        result = write_file(path, TestData)
        self.assertTrue(result and os.path.isfile(path))
        deleted = delete_file(path)
        self.assertFalse(os.path.isfile(path))
        self.assertTrue(deleted)
        self._msg('path', path)
        self._msg('exists', os.path.isfile(path))


    def test_uri_to_list(self):
        """
        Ensure uri_to_list function is working properly.
        """
        from minipylib.utils import uri_to_list
        self._msg('test', 'uri_to_list', first=True)
        uri = '/'
        result = uri_to_list(uri)
        expected = ['']
        self.assertEqual(result, expected)
        self._msg('uri', uri)
        self._msg('result', result)

        uri = '/module/submodule/action/'
        result = uri_to_list(uri)
        expected = ['module', 'submodule', 'action']
        self.assertEqual(result, expected)
        self._msg('uri', uri)
        self._msg('result', result)

        uri = '/module/submodule//action/'
        result = uri_to_list(uri)
        expected = ['module', 'submodule', '', 'action']
        self.assertEqual(result, expected)
        self._msg('uri', uri)
        self._msg('result', result)

    def test_data_object(self):
        """
        Ensure DataObject is working properly.
        """
        from minipylib.utils import DataObject
        self._msg('test', 'DataObject', first=True)
        data = {
            'a': 1,
            'b': 2,
            'c': 3,
        }
        obj = DataObject(**data)
        for k, v in data.items():
            self.assertEqual(obj[k], v)
            self._msg(k, v)


    def test_config(self):
        """
        Ensure Config class is working properly.

        * TODO
        """
        self._msg('test', 'Config', first=True)
        self._msg('TODO', '')


    def test_safe_unicode(self):
        """
        Ensure safe_unicode function is working properly.
        """
        from minipylib.utils import safe_unicode
        self._msg('test', 'safe_unicode', first=True)

        txt = 'hello'
        result = safe_unicode(txt)
        expected = 'hello'
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

        txt = '你好'
        result = safe_unicode(txt)
        expected = '你好'
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

        txt = 2
        result = safe_unicode(txt)
        expected = '2'
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

        txt = True
        result = safe_unicode(txt)
        expected = 'True'
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

        txt = 'écriture 寫作'
        result = safe_unicode(txt)
        expected = 'écriture 寫作'
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

        txt = 'café'
        result = safe_unicode(txt)
        expected = 'café'
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

        txt = u'more caf\xe9'
        result = safe_unicode(txt)
        expected = 'more café'
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

        txt = 'Ivan Krstić'
        result = safe_unicode(txt)
        expected = 'Ivan Krstić'
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

        txt = u'Ivan Krsti\u0107'
        result = safe_unicode(txt)
        expected = 'Ivan Krstić'
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

        txt = b'\xe2\x82\xac20'
        result = safe_unicode(txt)
        expected = '€20'
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

        # ሴ
        txt = b'\xe1\x88\xb4'
        result = safe_unicode(txt)
        expected = u'\u1234'
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)


    def test_safe_str(self):
        """
        Ensure safe_str function is working properly.
        """
        from minipylib.utils import safe_str
        self._msg('test', 'safe_str', first=True)

        txt = 'écriture 寫作'
        result = safe_str(txt)
        expected = txt.encode('utf-8')
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

        txt = u'Ivan Krsti\u0107'
        result = safe_str(txt)
        expected = txt.encode('utf-8')
        #self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

        txt = 'Ivan Krstić'
        result = safe_str(txt)
        expected = b'Ivan Krsti\xc4\x87'
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

        txt = b'\xc3\xa9criture \xe5\xaf\xab\xe4\xbd\x9c'
        result = safe_str(txt)
        expected = 'écriture 寫作'.encode('utf-8')
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

    def test_create_log(self):
        """
        Ensure create_log function is working properly.
        """
        import re
        import tempfile
        from minipylib.utils import create_log, get_file_contents
        self._msg('test', 'create_log', first=True)
        tmpfile_dir = tempfile.gettempdir()
        filename = 'minipylib.test.log'
        path = os.path.join(tmpfile_dir, filename)
        if os.path.isfile(path):
            os.unlink(path)
        logfile = create_log(filename, path)
        exists = os.path.isfile(path)
        self.assertTrue(exists)
        msg = 'this is a test'
        logfile.debug(msg)
        log_data = get_file_contents(path)
        found = False
        for line in log_data.splitlines(True):
            if re.search(msg, line):
                found = True
                break
        self.assertTrue(found)
        self._msg('found in line', line)
        os.unlink(path)


    def test_str_conv(self):
        """
        Ensure s2b and b2s conversion functions are working properly.
        """
        from minipylib.utils import s2b, b2s
        self._msg('test', 'test_str_conv', first=True)

        txt1 = 'écriture 寫作'
        txt2 = 'Ivan Krstić'
        txt3 = '\u1234'
        txt4 = 'abc'
        
        data = [6, 3.14159, -5e8, 5e-3, -15.8, txt4, 'def', 'ghi',
                4321, txt1, txt2, txt3]
        data_bytes = [s2b(s) for s in data]
        data_reconverted = [b2s(s) for s in data_bytes]

        self._msg('data', data)
        for n, s in enumerate(data):
            self.assertTrue(isinstance(s,
                                       (float,
                                        six.integer_types,
                                        six.string_types,
                                        six.text_type)))
            self._msg(n, s)

        self._msg('data_bytes', data_bytes)
        for n, s in enumerate(data_bytes):
            self.assertTrue(isinstance(s, six.binary_type))
            self._msg(n, repr(s))

        self._msg('data_reconverted', data_reconverted)
        for n, s in enumerate(data_reconverted):
            expected = data[n]
            if isinstance(expected, (float, six.integer_types)):
                expected = str(expected)
            self.assertEqual(s, expected)
            self.assertTrue(isinstance(s, (six.string_types, six.text_type)))
            self._msg(n, s)
