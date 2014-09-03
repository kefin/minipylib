# -*- coding: utf-8 -*-
"""
minipylib.crypto

This module contains functions to encrypt/decode data, create hash
digests and generate random passwords/secret keys.

Encryption and decryption use the PyCrypto toolkit's AES encryption
functions and classes:

:see: https://www.dlitz.net/software/pycrypto/

"""

# created: 2012-06-25 Kevin Chan <kefin@makedostudio.com>
# updated: 2014-08-29 kchan

from __future__ import (absolute_import, unicode_literals)

import six
import os
import hashlib
import base64
import hmac
import string
import random

try:
    import cPickle as pickle
except ImportError:
    import pickle

from Crypto.Cipher import AES




### AES encryption/decryption

# def encryption_test(data):
#     """
#     encrypt/decrypt test
#     """
#     secret = 'abc'
#
#     cipher = Cipher(secret)
#     ciphertext = cipher.encrypt(data)
#
#     print "# password: %s" % secret
#     print "# iv: %s" % base64.b64encode(cipher.iv)
#     print "# digest: %s" % base64.b64encode(cipher.digest)
#     print "# encrypted:"
#     print base64.b64encode(ciphertext)
#
#     cipher = Cipher(secret)
#     plaintext = cipher.decrypt(ciphertext)
#
#     print "# iv: %s" % base64.b64encode(cipher.iv)
#     print "# digest: %s" % base64.b64encode(cipher.digest)
#     print "# decrypted:"
#     print plaintext


class CipherError(Exception):
    """
    Raised when there is an error in the Cipher encode/decode operation.
    """
    pass


class Cipher(object):
    """
    Encryption/decryption cipher object using AES (from PyCrypto).

    Reference links:

    PyCrypto
        * http://www.pycrypto.org/
        * https://www.dlitz.net/software/pycrypto/

    Eli Bendersky's website > AES encryption of files in Python with PyCrypto
        * http://bit.ly/KXmxJM

    Example usage::

        def encryption_test(data):
            '''
            encrypt/decrypt test
            '''
            secret = 'abc'

            cipher = Cipher(secret)
            ciphertext = cipher.encrypt(data)

            print "# password: %s" % secret
            print "# iv: %s" % base64.b64encode(cipher.iv)
            print "# digest: %s" % base64.b64encode(cipher.digest)
            print "# encrypted:"
            print base64.b64encode(ciphertext)

            cipher = Cipher(secret)
            plaintext = cipher.decrypt(ciphertext)

            print "# iv: %s" % base64.b64encode(cipher.iv)
            print "# digest: %s" % base64.b64encode(cipher.digest)
            print "# decrypted:"
            print plaintext


    Note: the hash and encrypt/decrypt functions require byte data so
    unicode text need to be encoded as bytes before feeding into this
    object.    
    """
    iv_size = AES.block_size
    mode = AES.MODE_CFB
    digest_mod = hashlib.sha256
    digest_size = 32

    def __init__(self, secret):
        """
        :param secret: secret password
        """
        self.set_secret(secret)
        self.iv = None
        self.digest = None

    def set_secret(self, secret):
        """
        Set secret password (if not supplied at initialization).

        :param secret: set password to use for encrypt/decrypt methods.
        """
        self.secret = secret
        self.key = self.gen_key(secret)

    @classmethod
    def gen_key(cls, secret):
        """
        Generate a fix-length key from secret password.

        * default is 32 byte key (from sha256)

        :param secret: secret password to generate key from
        :returns: 32-byte sha256 hash for use as AES encryption key
        """
        if not secret:
            raise CipherError("Empty encryption key")
        if not isinstance(secret, (six.binary_type, six.string_types)):
            raise CipherError("Bad encryption key type.")
        h = hashlib.sha256()
        h.update(secret)
        return h.digest()

    def make_digest(self, *args):
        """
        Return a message digest for arguments.
        """
        h = self.digest_mod()
        for arg in args:
            h.update(arg)
        return h.digest()

    def encrypt(self, plaintext):
        """
        Encrypt plaintext.

        :param plaintext: data to be encrypted
        :returns: ciphertext
        """
        if not self.key:
            raise CipherError("Empty encryption key.")
        self.iv = os.urandom(self.iv_size)
        cryptobj = AES.new(self.key, mode=self.mode, IV=self.iv)
        encrypted = self.iv + cryptobj.encrypt(plaintext)
        self.digest = self.make_digest(encrypted)
        return self.digest + encrypted

    def decrypt(self, data):
        """
        Decrypt ciphertext.

        :param data: ciphertext to be decrypted
        :returns: plaintext data
        """
        if not self.key:
            raise CipherError("Empty encryption key")
        if not isinstance(data, six.binary_type):
            raise CipherError("Bad data supplied to decrypt method.")
        self.digest = data[:self.digest_size]
        header = self.digest_size + self.iv_size
        try:
            self.iv = data[self.digest_size:header]
            assert len(self.iv) == self.iv_size
        except (IndexError, AssertionError):
            raise CipherError("Unable to retrieve IV.")
        ciphertext = data[header:]
        cryptobj = AES.new(self.key, mode=self.mode, IV=self.iv)
        decrypted = cryptobj.decrypt(ciphertext)
        if self.make_digest(data[self.digest_size:]) != self.digest:
            raise CipherError("Data signatures do not match!")
        return decrypted


### functions to encode/decode using AES Cipher object (above)

### example encode/decode function
#
# def encoder(data, secret, mode):
#     """
#     encrypt or decrypt data.
#
#     :param data: data to be encoded/decoded
#     :param secret: secret password
#     :param mode: 'e' (encode) or 'd' (decode)
#     :returns: encoded/decoded data
#     """
#     if mode == 'd':
#         plaintext = decode_data(data, secret, b64_encoding=True)
#         print plaintext
#     else:
#         ciphertext = encode_data(data, secret, b64_encoding=True)
#         print ciphertext


Encoders = {
    'base16': base64.b16encode,
    'base32': base64.b32encode,
    'base64': base64.b64encode
}

Decoders = {
    'base16': base64.b16decode,
    'base32': base64.b32decode,
    'base64': base64.b64decode
}


def get_encoder(encode):
    """
    Return encoder corresponding to encode string or callable.

    :param encoding: string (either 'base16', 'base32' or 'base64') or callable
    :returns: callable
    """
    if callable(encode):
        return encode
    try:
        encoder = Encoders.get(encode)
    except (TypeError, KeyError):
        encoder = None
    return encoder


def get_decoder(decode):
    """
    Return decoder corresponding to decode string or callable.

    :param encoding: string (either 'base16', 'base32' or 'base64') or callable
    :returns: callable
    """
    if callable(decode):
        return decode
    try:
        decoder = Decoders.get(decode)
    except (TypeError, KeyError):
        decoder = None
    return decoder


def encode_data(data, secret_key, pickle_data=False, encoding=None):
    """
    Encode data using encryption, pickle and base64.b64encode.

    :param data: data to encrypt (set pickle_data to True if Python data structure).
    :param pickle_data: True or False; set to True to enable pickling.
    :param encoding: use base16, basse32 or base64 encoding
    :returns: string
    """
    if pickle_data:
        data = pickle.dumps(data)
    encoded = Cipher(secret_key).encrypt(data)
    encoder = get_encoder(encoding)
    if callable(encoder):
        encoded = encoder(encoded)
    return encoded


def decode_data(encrypted, secret_key, pickle_data=False, encoding=None):
    """
    Decode data encrypted and encoded by encode_data above.

    :param encrypted: encoded string to be decoded.
    :param pickle_data: True or False; set to True if encrypted data is  pickled.
    :param encoding: use base16, basse32 or base64 encoding
    :returns: data structure.
    """
    decoder = get_decoder(encoding)
    if callable(decoder):
        encrypted = decoder(encrypted)
    decoded = Cipher(secret_key).decrypt(encrypted)
    if pickle_data:
        decoded = pickle.loads(decoded)
    return decoded


### hash functions

DefaultHash = hashlib.sha256
DefaultHashAlgorithms = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'sha224': hashlib.sha224,
    'sha256': hashlib.sha256,
    'sha384': hashlib.sha384,
    'sha512': hashlib.sha512
}

def file_digest(path, block_size=2**10, hashfunc=None, algorithm=None):
    """
    Calculate hash for file (default algorithm is hashlib.sha256).

    :param path: file system path for file
    :param hashfunc: algorithm to use (from hashlib)
    :param algorithm: alternative method of specifying hash algorithm (as string)
    :returns: hash in hex
    """
    from minipylib.utils import open_file
    if hashfunc is None:
        if algorithm is None:
            hashfunc = DefaultHash
        else:
            hashfunc = DefaultHashAlgorithms.get(algorithm, DefaultHash);

    hasher = hashfunc()
    with open_file(path, mode='rb') as file_obj:
        while True:
            data = file_obj.read(block_size)
            if not data:
                break
            hasher.update(data)

    return hasher.hexdigest()


def md5_for_file(path, block_size=2**10):
    """
    Calculate md5 checksum for file.

    :param path: file system path for file
    :returns: md5 hash in hex
    """
    return file_digest(path, block_size=block_size, hashfunc=hashlib.md5)



### make hmac digest

def make_digest(secret_key, *args, **kwargs):
    """
    Return an ``HMAC`` digest for arguments.

    :param secret_key: secret password to use for creating hash digest
    :param args: a list of byte strings to calculate digest from
    :param digestmod: keyword argument for digest module (default: DefaultHash)
    :param hexdigest: if True, return hexdigest format, else regular binary
    :returns: digest (in hexdigest format if ``hexdigest`` is set to True)

    Note: HMAC does not accept unicode (in PY3) so ``secret_key`` must
    be a byte string.

    See this comment from: http://bugs.python.org/issue16063#msg172263

        HMAC and all cryptographic hashing algorithms work with bytes
        only. Text (unicode) is neither specified by the standards nor
        supported. You have to convert your text to bytes with some
        encoding (e.g. ASCII or UTF-8).

    :More info:

        * http://stackoverflow.com/questions/20849805/python-hmac-typeerror-character-mapping-must-return-integer-none-or-unicode
        * http://bugs.python.org/issue5285
        * http://bugs.python.org/issue16063

    """
    digestmod = kwargs.get('digestmod', DefaultHash)
    hasher = hmac.new(secret_key, digestmod=digestmod)
    for arg in args:
        hasher.update(arg)
    if kwargs.get('hexdigest') is True:
        return hasher.hexdigest()
    return hasher.digest()


### secret key generation

DEFAULT_KEY_SIZE = 72
SECRET_KEY_CHAR_SET = 'anp'
DEFAULT_KEY_CHAR_SET = 'an'

csets = {
    'a': string.ascii_letters,
    'l': string.ascii_lowercase,
    'u': string.ascii_uppercase,
    'n': string.digits,
    'p': string.punctuation,
}

def gen_secret_key(keysize=DEFAULT_KEY_SIZE,
                   charset=DEFAULT_KEY_CHAR_SET,
                   key_string=None):
    """
    Returns a random ascii string of length ``keysize``

    :param keysize: length of key to generate (default is 72)
    :param charset: string of character sets to use (a, l, u, n, p)
    :param key_string: use provided string for key characters
    :returns: random string or None if error

    Caller should specify character set to use: ::

        a: ascii letters
        u: ascii uppercase letters
        l: ascii lowercase letters
        n: numerals
        p: punctuations

    Example: Generate a 64-character key consisting of lowercase
    ascii + digits: ::

        key = gen_secret_key(64, charset='ln')

    If ``key_string`` is specified, function will ignore ``charset``
    parameter.

    For non-ascii characters, supply custom key string in ``key_string``.
    example: ::

        import string
        key = gen_secret_key(64, key_string=string.letters+string.digits)

    """
    if key_string and isinstance(key_string, six.string_types):
        chars = key_string
    else:
        chars = ''
        added = {}
        for c in charset:
            if not c in added:
                added[c] = True
                if c in ('a', 'l', 'u', 'n', 'p'):
                    if c == 'a':
                        added['u'] = True
                        added['l'] = True
                    chars += csets.get(c, '')
    try:
        keysize = int(keysize)
        assert keysize > 0
    except (TypeError, ValueError, AssertionError):
        key = None
    else:
        prng = random.SystemRandom()
        key = ''.join([prng.choice(chars) for i in range(keysize)])
    return key
