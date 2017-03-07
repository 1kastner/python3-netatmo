#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# System modules
import os
from setuptools import setup, find_packages

def read_file(file):
    """ Read file relative to this file
    """
    with open(os.path.join(os.path.dirname(__file__),file)) as f:
        return f.read()

# run setup
# take metadata from setup.cfg
setup( 
    name = 'netatmo',
    version = '0.1.0',
    description = 'access to netatmo api',
    long_description = read_file("README.md"),
    keywords = [ 'netatmo','api' ],
    license = 'GPLv3',
    author = 'Yann Büchau',
    author_email = 'yann.buechau@web.de',
    url = 'https://github.com/nobodyinperson/python3-netatmo',
    classifiers = [
	'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
	'Programming Language :: Python :: 3.5',
	'Operating System :: OS Independent',
	'Topic :: Home Automation',
	'Topic :: Internet',
	'Topic :: Scientific / Engineering',
	'Topic :: Scientific/Engineering :: Atmospheric Science',
	'Topic :: Software Development :: Libraries :: Python Modules',
	'Topic :: Utilities',
        ],
    test_suite = 'tests',
    tests_require = [ 'pandas', 'numpy' ],
    install_requires = [ 'pandas', 'numpy' ],
    packages = find_packages(exclude=['tests']),
    )

