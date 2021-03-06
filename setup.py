"""
setup.py
* setup.py for minipylib

* created: 2011-01-11 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-09-01 kchan
"""

from setuptools import setup, find_packages

setup(
	name = "minipylib",
	version = "0.2.9",
	packages = find_packages(),
	author = "Kevin Chan",
	author_email = "kefin@makedostudio.com",
	description = "A small library of utility functions for Python web development",
    long_description='Minipylib is a small library of utility functions useful for developing python web applications.',
	url = "",
	license = "BSD",
	platforms = 'any',
	include_package_data = True,

	install_requires = ['markdown', 'textile', 'PyYaml', 'pycrypto', 'nose'],
)
