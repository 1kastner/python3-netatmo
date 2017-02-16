# -*- coding: utf-8 -*-
# System modules
import os
import shutil
import logging
import unittest
import json
from functools import wraps

# External modules

# Internal modules
from .test_data import *

# get a logger
logger = logging.getLogger(__name__)


####################################
### all tests should import this ###
####################################

# basic test class with utilities
class BasicTest(unittest.TestCase):
    pass


# in the beginning of a test module, do all this
# *this is used by the unittest module*
def setUpModule():
    # create the test directory
    if not os.path.exists(TMPDIR):
        logger.debug("creating TMPDIR '{}'".format(TMPDIR))
        os.makedirs(TMPDIR)
    
# in the end of this a module, do all this
# *this is used by the unittest module*
def tearDownModule():
    # remove the test directory
    if os.path.exists(TMPDIR):
        logger.debug("removing TMPDIR '{}'".format(TMPDIR))
        shutil.rmtree(TMPDIR)


# test decorator
# decorate every test method with this
# the test name will be printed in INFO context before and after the test
def testname(name="unnamed"):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            logger.info("--- [start] »{}« test ---".format(name))
            res = f(*args, **kwargs)
            logger.info("--- [done ] »{}« test ---".format(name))
            return res
        return wrapped
    return decorator


# read json from a filename
def read_json_from_file(filename):
    """
    read json from a file given then filename
    args:
        filename (str): The path to the file to read
    returns:
        dict, empty dict if error occured during read
    """
    try: # open and read, return result
        with open(filename, "r") as f:
            return json.load(f)
    except: # didn't work, return empty dict
        return {}
