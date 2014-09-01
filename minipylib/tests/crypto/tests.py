# -*- coding: utf-8 -*-
"""
tests.crypto.tests

Tests for minipylib.crypto

* created: 2014-08-29 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-09-01 kchan
"""

from __future__ import (absolute_import, unicode_literals)

from minipylib.tests.helpers import SimpleTestCase


class CryptoTests(SimpleTestCase):

    def test_cipher(self):
        """
        Ensure Cipher class is working properly.
        """
        import base64
        from minipylib.crypto import Cipher, CipherError

        self._msg('test', 'Cipher', first=True)

        secret_key = 'the-secret-key'
        data = 'Attack at dawn.'
        enc_cipher = Cipher(secret_key)
        ciphertext = enc_cipher.encrypt(data)
        self._msg('secret_key', secret_key)
        self._msg('data', data)
        self._msg('iv size', enc_cipher.iv_size)
        self._msg('iv (b64)', base64.b64encode(enc_cipher.iv))
        self._msg('ciphertext (b64)', base64.b64encode(ciphertext))

        dec_cipher = Cipher(secret_key)
        plaintext = dec_cipher.decrypt(ciphertext)
        self.assertEqual(plaintext, data)
        self._msg('plaintext', plaintext)

        dec_cipher = Cipher(secret_key)
        self.assertRaises(CipherError, dec_cipher.decrypt, "abc")


    def test_cipher_defaults(self):
        """
        Ensure Cipher default settings are correct."
        """
        import hashlib
        from Crypto.Cipher import AES
        from minipylib.crypto import Cipher
        self._msg('test', 'Cipher default settings', first=True)

        secret_key = "the-secret-key"
        cipher = Cipher(secret_key)
        self.assertEqual(cipher.iv_size, AES.block_size)
        self.assertEqual(cipher.mode, AES.MODE_CFB)
        self.assertEqual(cipher.digest_mod, hashlib.sha256)
        self.assertEqual(cipher.digest_size, 32)

        self._msg('iv_size', cipher.iv_size)
        self._msg('mode', cipher.mode)
        self._msg('digest_mod', cipher.digest_mod)
        self._msg('digest_size', cipher.digest_size)


    def test_cipher_set_secret(self):
        """
        Ensure Cipher.set_secret method is working properly.
        """
        import base64
        from minipylib.crypto import Cipher
        self._msg('test', 'Cipher.set_secret()', first=True)

        secret_key = 'the-secret-key'
        data = 'Attack at dawn.'
        enc_cipher = Cipher(secret_key)
        self.assertEqual(enc_cipher.secret, secret_key)
        
        secret_key2 = 'a different secret key'
        enc_cipher.set_secret(secret_key2)
        self.assertEqual(enc_cipher.secret, secret_key2)

        ciphertext = enc_cipher.encrypt(data)
        self._msg('secret_key', secret_key)
        self._msg('secret_key2', secret_key2)
        self._msg('data', data)
        self._msg('iv size', enc_cipher.iv_size)
        self._msg('iv (b64)', base64.b64encode(enc_cipher.iv))
        self._msg('ciphertext (b64)', base64.b64encode(ciphertext))

        dec_cipher = Cipher(secret_key)
        plaintext = dec_cipher.decrypt(ciphertext)
        self.assertNotEqual(base64.b64encode(plaintext), base64.b64encode(data))
        self._msg('plaintext', repr(plaintext))

        dec_cipher = Cipher(secret_key2)
        plaintext = dec_cipher.decrypt(ciphertext)
        self.assertEqual(plaintext, data)
        self.assertEqual(base64.b64encode(plaintext), base64.b64encode(data))
        self._msg('plaintext', repr(plaintext))


    def test_cipher_gen_key(self):
        """
        Ensure Cipher.gen_key method is working properly.
        """
        import base64
        from minipylib.crypto import Cipher, CipherError
        self._msg('test', 'Cipher.gen_key()', first=True)

        secret_key = 'the-secret-key'
        digest = Cipher.gen_key(secret_key)
        self._msg('secret_key', secret_key)
        self._msg('digest', repr(digest))
        self._msg('digest len', len(digest))
        self.assertEqual(len(digest), 32)

        secret_key = 'a'
        digest = Cipher.gen_key(secret_key)
        self._msg('secret_key', secret_key)
        self._msg('digest', repr(digest))
        self._msg('digest len', len(digest))
        self.assertEqual(len(digest), 32)

        secret_key = 12
        self.assertRaises(CipherError, Cipher.gen_key, secret_key)

        secret_key = None
        self.assertRaises(CipherError, Cipher.gen_key, secret_key)

        secret_key = ["abc"]
        self.assertRaises(CipherError, Cipher.gen_key, secret_key)

        secret_key = {"key": 12}
        self.assertRaises(CipherError, Cipher.gen_key, secret_key)


    def test_get_encoder(self):
        """
        Ensure get_encoder function is working properly.
        """
        import base64
        from minipylib.crypto import Encoders, get_encoder
        self._msg('test', 'get_encoder', first=True)
        encoders = {
            'base16': base64.b16encode,
            'base32': base64.b32encode,
            'base64': base64.b64encode
        }
        for name, encoder in encoders.items():
            e = get_encoder(name)
            self.assertEqual(e, encoder)
            self._msg(name, encoder)

        def my_encoder(data):
            return 'test'

        e = get_encoder(my_encoder)
        self.assertEqual(e, my_encoder)
        self._msg('my_encoder', e)


    def test_get_decoder(self):
        """
        Ensure get_decoder function is working properly.
        """
        import base64
        from minipylib.crypto import Decoders, get_decoder
        self._msg('test', 'get_decoder', first=True)
        decoders = {
            'base16': base64.b16decode,
            'base32': base64.b32decode,
            'base64': base64.b64decode
        }
        for name, decoder in decoders.items():
            d = get_decoder(name)
            self.assertEqual(d, decoder)
            self._msg(name, decoder)

        def my_decoder(data):
            return 'test'

        d = get_decoder(my_decoder)
        self.assertEqual(d, my_decoder)
        self._msg('my_decoder', d)


    def test_encode_data(self):
        """
        Ensure encode_data function is working properly.
        """
        from minipylib.crypto import encode_data, decode_data
        self._msg('test', 'encode_data', first=True)
        secret_key = 'secret-key'
        data = 'Attack at dawn.'
        encoded = encode_data(data, secret_key, encoding='base64')
        decoded = decode_data(encoded, secret_key, encoding='base64')
        self.assertEqual(decoded, data)
        self._msg('data', data)
        self._msg('encoded', encoded)
        self._msg('decoded', decoded)


    def test_decode_data(self):
        """
        Ensure decode_data function is working properly.
        """
        self._msg('test', 'decode_data', first=True)
        from minipylib.crypto import decode_data
        secret_key = 'secret-key'
        encoded = 'W+ryRfcON4HcWbwoO+25vprJF+D7GcLHDAZ1p5UCJMTm+wd4y3xL966XX/BkldyCNlHYBo1wuitT/+H9DSPU'
        expected = 'Attack at dawn.'
        decoded = decode_data(encoded, secret_key, encoding='base64')
        self.assertEqual(decoded, expected)
        self._msg('data', expected)
        self._msg('encoded', encoded)
        self._msg('decoded', decoded)


    def test_file_digest(self):
        """
        Ensure file_digest function is working properly.
        """
        import os
        from minipylib.crypto import file_digest
        self._msg('test', 'file_digest', first=True)
        module_dir = os.path.dirname(os.path.realpath(__file__))
        filename = 'example_message.txt'
        digest = '1d6c270d7cc7e82a816ffb7bc3797d213b24d9d17af48f4b3b8d01fb43ed15c3'
        path = os.path.join(module_dir, filename)
        d = file_digest(path)
        self.assertEqual(d, digest)
        self._msg('path', path)
        self._msg('expected', digest)
        self._msg('digest', d)

        d = file_digest(path, algorithm='sha512')
        digest = 'b42138c86cde82bdae583ee2769903b57e41a0f125531a16dfcdaa42aa6e531d3d7a225facd629c27468b090475f1c62fb03aaf20d2466a88d1f9269605a7478'
        self.assertEqual(d, digest)
        self._msg('path', path)
        self._msg('expected', digest)
        self._msg('digest', d)


    def test_md5_for_file(self):
        """
        Ensure md5_for_file function is working properly.
        """
        import os
        from minipylib.crypto import file_digest, md5_for_file
        self._msg('test', 'md5_for_file', first=True)
        module_dir = os.path.dirname(os.path.realpath(__file__))
        filename = 'example_message.txt'
        path = os.path.join(module_dir, filename)
        expected = file_digest(path, algorithm='md5')
        digest = md5_for_file(path)
        self.assertEqual(digest, expected)
        self._msg('path', path)
        self._msg('expected', expected)
        self._msg('digest', digest)


    def test_make_digest(self):
        """
        Ensure make_digest function is working properly.
        """
        from minipylib.crypto import make_digest
        self._msg('test', 'make_digest', first=True)
        txt = 'écriture 寫作'
        secret_key = txt
        data = ['abc', 'def', 'ghi', '4321']
        digest = make_digest(secret_key, 'abc', hexdigest=True)
        expected = '6426a4b12a28ff6896e1383a6952167380a50d345b3e2af8c9f7ce5b28bc6804'
        self.assertEqual(digest, expected)
        self._msg('data', repr(data))
        self._msg('expected', expected)
        self._msg('digest', digest)


    def test_gen_secret_key(self):
        """
        Ensure gen_scret_key function is working properly.
        """
        import string
        from minipylib.crypto import gen_secret_key, DEFAULT_KEY_CHAR_SET
        self._msg('test', 'gen_secret_key', first=True)

        def in_set(cset, txt):
            result = 0
            for c in txt:
                if c in cset:
                    result += 1
            return result

        # default key character set is alphanumeric
        keylen = 99
        charset = DEFAULT_KEY_CHAR_SET
        secret = gen_secret_key(keysize=keylen)
        chlen = in_set(string.ascii_letters + string.digits, secret)
        self.assertEqual(len(secret), keylen)
        self.assertEqual(chlen, keylen)
        self._msg('secret len', len(secret))
        self._msg('charset', charset)
        self._msg('in set', chlen)
        self._msg('secret', secret)

        # alpha lowercase + digits
        keylen = 19
        charset = 'ln'
        secret = gen_secret_key(keysize=keylen, charset=charset)
        chlen = in_set(string.ascii_lowercase + string.digits, secret)
        self.assertEqual(len(secret), keylen)
        self.assertEqual(chlen, keylen)
        self._msg('secret len', len(secret))
        self._msg('charset', charset)
        self._msg('in set', chlen)
        self._msg('secret', secret)

        keylen = 28
        charset = 'lnlnlnln'
        secret = gen_secret_key(keysize=keylen, charset=charset)
        chlen = in_set(string.ascii_lowercase + string.digits, secret)
        self.assertEqual(len(secret), keylen)
        self.assertEqual(chlen, keylen)
        self._msg('secret len', len(secret))
        self._msg('charset', charset)
        self._msg('in set', chlen)
        self._msg('secret', secret)

        # alpha lowercase + digits + punctuation
        keylen = 19
        charset = 'lnp'
        secret = gen_secret_key(keysize=keylen, charset=charset)
        chlen = in_set(string.ascii_lowercase + string.digits + string.punctuation,
                       secret)
        self.assertEqual(len(secret), keylen)
        self.assertEqual(chlen, keylen)
        self._msg('secret len', len(secret))
        self._msg('charset', charset)
        self._msg('in set', chlen)
        self._msg('secret', secret)

        keylen = 191
        charset = 'nppppllllnplll'
        secret = gen_secret_key(keysize=keylen, charset=charset)
        chlen = in_set(string.ascii_lowercase + string.digits + string.punctuation,
                       secret)
        self.assertEqual(len(secret), keylen)
        self.assertEqual(chlen, keylen)
        self._msg('secret len', len(secret))
        self._msg('charset', charset)
        self._msg('in set', chlen)
        self._msg('secret', secret)

        # alpha upper + digits + punctuation
        keylen = 19
        charset = 'unp'
        secret = gen_secret_key(keysize=keylen, charset=charset)
        chlen = in_set(string.ascii_uppercase + string.digits + string.punctuation,
                       secret)
        self.assertEqual(len(secret), keylen)
        self.assertEqual(chlen, keylen)
        self._msg('secret len', len(secret))
        self._msg('charset', charset)
        self._msg('in set', chlen)
        self._msg('secret', secret)

        keylen = 19
        charset = 'unpuuppppppn'
        secret = gen_secret_key(keysize=keylen, charset=charset)
        chlen = in_set(string.ascii_uppercase + string.digits + string.punctuation,
                       secret)
        self.assertEqual(len(secret), keylen)
        self.assertEqual(chlen, keylen)
        self._msg('secret len', len(secret))
        self._msg('charset', charset)
        self._msg('in set', chlen)
        self._msg('secret', secret)


        # alpha upper + lower + digits + punctuation
        keylen = 72
        charset = 'unplapaassdsp'
        secret = gen_secret_key(keysize=keylen, charset=charset)
        chlen = in_set(string.ascii_uppercase + string.lowercase \
                       + string.digits + string.punctuation,
                       secret)
        self.assertEqual(len(secret), keylen)
        self.assertEqual(chlen, keylen)
        self._msg('secret len', len(secret))
        self._msg('charset', charset)
        self._msg('in set', chlen)
        self._msg('secret', secret)

        keylen = 191
        charset = 'unpuuppppppnuapl'
        secret = gen_secret_key(keysize=keylen, charset=charset)
        chlen = in_set(string.ascii_uppercase + string.lowercase \
                       + string.digits + string.punctuation,
                       secret)
        self.assertEqual(len(secret), keylen)
        self.assertEqual(chlen, keylen)
        self._msg('secret len', len(secret))
        self._msg('charset', charset)
        self._msg('in set', chlen)
        self._msg('secret', secret)

        # default key character set is alphanumeric
        keylen = 99
        key_string = 'abcd98765@'
        secret = gen_secret_key(keysize=keylen, key_string=key_string)
        chlen = in_set(key_string, secret)
        self.assertEqual(len(secret), keylen)
        self.assertEqual(chlen, keylen)
        self._msg('secret len', len(secret))
        self._msg('key_string', key_string)
        self._msg('in set', chlen)
        self._msg('secret', secret)

        keylen = 99
        key_string = 'abcd' + string.punctuation
        secret = gen_secret_key(keysize=keylen, key_string=key_string)
        chlen = in_set(key_string, secret)
        self.assertEqual(len(secret), keylen)
        self.assertEqual(chlen, keylen)
        self._msg('secret len', len(secret))
        self._msg('key_string', key_string)
        self._msg('in set', chlen)
        self._msg('secret', secret)

        # bad keylen
        keylen = -721
        secret = gen_secret_key(keysize=keylen)
        self.assertTrue(secret is None)
        self._msg('keylen', keylen)
        self._msg('secret', secret)
