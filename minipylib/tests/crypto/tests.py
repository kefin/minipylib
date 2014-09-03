# -*- coding: utf-8 -*-
"""
tests.crypto.tests

Tests for minipylib.crypto

* created: 2014-08-29 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-09-01 kchan
"""

from __future__ import (absolute_import, unicode_literals)

from minipylib.tests.helpers import SimpleTestCase


# from project gutenberg:
# http://www.gutenberg.org/ebooks/12479

example_text_file = 'san-zi-jing.txt'
example_text = """\
Title:San Zi Jing[220-581 A.D.]

Author:anonymous

Release Date:220-581 A.D.

Language: Chinese

Produced by Yu Ya-chu

《三字經》

人之初，性本善。性相近，習相遠。苟不教，性乃遷。教之道，貴以專。昔孟母，擇鄰處。子不學，斷機杼。竇燕山，有義方。教五子，名俱揚。養不教，父之過。教不嚴，師之惰。子不學，非所宜。幼不學，老何為。玉不琢，不成器。人不學，不知義。為人子，方少時。親師友，習禮儀。香九齡，能溫席。孝於親，所當執。融四歲，能讓梨。弟于長，宜先知。首孝弟，次見聞。知某數，識某文。一而十，十而百。百而千，千而萬。三才者，天地人。三光者，日月星。三綱者，君臣義。父子親，夫婦順。曰春夏，曰秋冬。此四時，運不窮。曰南北，曰西東。此四方，應乎中。曰水火，木金土。此五行，本乎數。曰仁義，禮智信。此五常，不容紊。稻粱菽，麥黍稷。此六穀，人所食。馬牛羊，雞犬豕。此六畜，人所飼。曰喜怒，曰哀懼。愛惡欲，七情具。□土革，木石金。與絲竹，乃八音。高曾祖，父而身。身而子，子而孫。自子孫，至元曾。乃九族，而之倫。父子恩，夫婦從。兄則友，弟則恭。長幼序，友與朋。君則敬，臣則忠。此十義，人所同。
凡訓蒙，須講究。詳訓詁，名句讀。為學者，必有初。小學終，至四書。論語者，二十篇。群弟子，記善言。孟子者，七篇止。講道德，說仁義。作中庸，子思筆。中不偏，庸不易。作大學，乃曾子。自修齊，至平治。孝經通，四書熟。如六經，始可讀。詩書易，禮春秋。號六經，當講求。有連山，有歸藏。有周易，三易詳。有典謨，有訓誥。有誓命，書之奧。我周公，作周禮。著六官，存治體。大小戴，注禮記。述聖言，禮樂備。曰國風，曰雅頌。號四詩，當諷詠。詩既亡，春秋作。寓褒貶，別善惡。三傳者，有公羊。有左氏，有彀梁。經既明，方讀子。撮其要，記其事。五子者，有荀楊。文中子，及老莊。
經子通，讀諸史。考世系，知終始。自羲農，至黃帝。號三皇，居上世。唐有虞，號二帝。相揖遜，稱盛世。夏有禹，商有湯。周文王，稱三王。夏傳子，家天下。四百載，遷夏社。湯伐夏，國號商。六百載，至紂亡。周武王，始誅紂。八百載，最長久。周轍東，王綱墮。逞干戈，尚遊說。始春秋，終戰國。五霸強，七雄出。嬴秦氏，始兼併。傳二世，楚漢爭。高祖興，漢業建。至孝平，王莽篡。光武興，為東漢。四百年，終於獻。魏蜀吳，爭漢鼎。號三國，迄兩晉。宋齊繼，梁陳承。為南朝，都金陵。北元魏，分東西。宇文周，興高齊。迨至隋，一土宇。不再傳，失統緒。唐高祖，起義師。除隋亂，創國基。二十傳，三百載。梁義之，國乃改。炎宋興，受周禪。十八傳，南北混。遼于金，皆稱帝。太祖興，國大明。號洪武，都金陵。迨成祖，遷燕京。十六世，至崇禎。閹亂後，寇內訌。闖逆變，神器終。清順治，據神京。至十傳，宣統遜。舉總統，共和成。複漢土，民國興。
廿二史，全在茲。載治亂，知興衰。讀史書，考實錄。通古今，若親目。口而誦，心而惟。朝于斯，夕於斯。昔仲尼，師項□。古聖賢，尚勤學。趙中令，讀魯論。彼既仕，學且勤。披蒲編，削竹簡。彼無書，且知勉。頭懸樑，錐刺股。彼不教，自勤苦。如囊螢，如映雪。家雖貧，學不綴。如負薪，如掛角。身雖勞，猶苦卓。蘇老泉，二十七。始發憤，讀書籍。彼既老，猶悔遲。爾小生，宜早思。若梁□，八十二。對大廷，魁多士。彼既成，眾稱異。爾小生，宜立志。瑩八歲，能詠詩。泌七歲，能賦□。彼穎悟，人稱奇。爾幼學，當效之。蔡文姬，能辨琴。謝道□，能詠吟。彼女子，且聰敏。爾男子，當自警。唐劉晏，方七歲。舉神童，作正字。彼雖幼，身己仕。爾幼學，勉而致。有為者，亦若是。
犬守夜，雞司晨。苟不學，曷為人。蠶吐絲，蜂釀蜜。人不學，不如物。幼而學，壯而行。上致君，下澤民。揚名聲，顯父母。光于前，裕於後。人遺子，金滿嬴。我教子，惟一經。勤有功，戲無益。戒之哉，宜勉力。
"""


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
        from minipylib.utils import s2b, b2s
        self._msg('test', 'encode_data', first=True)
        secret_key = 'secret-key'
        data = 'Attack at dawn.'
        encoded = encode_data(data, secret_key, encoding='base64')
        decoded = decode_data(encoded, secret_key, encoding='base64')
        self.assertEqual(decoded, data)
        self._msg('data', data)
        self._msg('encoded', encoded)
        self._msg('decoded', decoded)

        # test encoded_data on unicode text
        # * make sure to convert all unicode text to bytes first
        secret_key = 'secret-key'
        original_text = example_text
        data = s2b(original_text)
        encoded = encode_data(data, secret_key, encoding='base64')
        decoded = decode_data(encoded, secret_key, encoding='base64')
        decoded = b2s(decoded)
        self.assertEqual(decoded, original_text)
        equal = decoded == original_text
        self._msg('data', data)
        self._msg('encoded', encoded)
        self._msg('decoded', decoded)
        self._msg('equal', equal)


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
        import tempfile
        from minipylib.crypto import file_digest, DefaultHash
        from minipylib.utils import open_file, write_file, s2b, b2s

        self._msg('test', 'file_digest', first=True)

        # 1. test a simple message
        module_dir = os.path.dirname(os.path.realpath(__file__))
        filename = 'example_message.txt'
        digest = '1d6c270d7cc7e82a816ffb7bc3797d213b24d9d17af48f4b3b8d01fb43ed15c3'
        path = os.path.join(module_dir, filename)
        d = file_digest(path)
        self.assertEqual(d, digest)
        self._msg('path', path)
        self._msg('* expected', digest)
        self._msg('* digest', d)

        # 2. test a file containing Traditional Chinese unicode text

        # write example_text to temporary file and calculate digest
        self._msg('write example_text to temporary file and calculate digest')
        filename = 'test_file_digest_example_data.txt'
        tmpfile_dir = tempfile.gettempdir()
        path = os.path.join(tmpfile_dir, filename)
        result = write_file(path, example_text)
        self.assertTrue(result)
        self._msg('path', path)

        h2 = DefaultHash()
        f = open(path, 'rb')
        block_size = 2**10
        while True:
            data = f.read(block_size)
            if not data:
                break
            h2.update(data)
        f.close()
        digest = h2.hexdigest()
        self._msg('* digest', digest)

        expected = digest
        digest = file_digest(path)
        self._msg('path', path)
        self._msg('* digest', digest)
        self.assertEqual(digest, expected)

        # delete temp file
        os.unlink(path)

        # 3. test digest against example file in test directory
        filename = example_text_file
        path = os.path.join(module_dir, filename)
        with open_file(path, mode='rb') as file_obj:
            data_from_file = file_obj.read()

        # convert to unicode string and compare with exxample_text
        data_from_file = b2s(data_from_file)
        self._msg('path', path)
        self.assertEqual(data_from_file, example_text)
        equal = data_from_file == example_text
        self._msg('* equal to orig', equal)

        # calculate file digest of test directory file with
        # digest of temporary file (containing the same text)
        digest = file_digest(path)
        self.assertEqual(digest, expected)
        self._msg('path', path)
        self._msg('* expected', expected)
        self._msg('* digest', digest)


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

        # test             : make_digest
        # secret_key       : écriture 寫作
        # secret_key_bytes : '\xc3\xa9criture \xe5\xaf\xab\xe4\xbd\x9c'
        # data             : [3.14159, u'abc', u'def', u'ghi', u'4321', u'\xe9criture \u5beb\u4f5c', u'\u1234']
        # digest_data      : ['3.14159', 'abc', 'def', 'ghi', '4321', '\xc3\xa9criture \xe5\xaf\xab\xe4\xbd\x9c', '\xe1\x88\xb4']
        # expected         : 88eb22670a7e9a454df26670ce0ff9838013fabfedac978a4c2539b7a3db9de9
        # digest           : 88eb22670a7e9a454df26670ce0ff9838013fabfedac978a4c2539b7a3db9de9

        """
        from minipylib.crypto import make_digest
        from minipylib.utils import s2b
        self._msg('test', 'make_digest', first=True)
        secret_key = 'écriture 寫作'
        data = [3.14159, 'abc', 'def', 'ghi', '4321', 'écriture 寫作', '\u1234']
        # convert secret_key and data using s2b (string-to-bytes) function
        # before feeding to make_digest.
        secret_key_bytes = s2b(secret_key)
        digest_data = [s2b(s) for s in data]
        digest = make_digest(secret_key_bytes, *digest_data, hexdigest=True)
        expected = '88eb22670a7e9a454df26670ce0ff9838013fabfedac978a4c2539b7a3db9de9'
        self.assertEqual(digest, expected)
        self._msg('secret_key', secret_key)
        self._msg('secret_key_bytes', repr(secret_key_bytes))
        self._msg('data', data)
        self._msg('digest_data', digest_data)
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
