#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# System modules
import os
from setuptools import setup, find_packages

from netatmo import __version__

def read_file(filename):
    with open(filename) as f:
        return f.read()

# run setup
# take metadata from setup.cfg
setup( 
    name = "netatmo",
    description = "painless access to the netatmo weather api",
    long_descrpition = read_file("README.rst"),
    author = "Yann Büchau",
    author_email = "yann.buechau@web.de",
    keywords = "netatmo, api",
    version = __version__,
    license = 'GPLv3',
    url = 'https://github.com/nobodyinperson/python3-netatmo',
    classifiers = [
	'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
	'Programming Language :: Python :: 3.5',
	'Operating System :: OS Independent',
	'Topic :: Home Automation',
	'Topic :: Internet',
	'Topic :: Scientific/Engineering :: Atmospheric Science',
	'Topic :: Software Development :: Libraries :: Python Modules',
	'Topic :: Utilities',
        ],
    test_suite = 'tests',
    tests_require = [ 'pandas', 'numpy' ],
    install_requires = [ 'pandas', 'numpy' ],
    packages = find_packages(exclude=['tests']),
    )

