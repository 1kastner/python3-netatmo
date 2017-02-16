#!/usr/bin/env python3
# system modules
import unittest
import logging
import os
import shutil
import json

# import utils module
from netatmo import utils
# import test data
from .test_data import *
from .test_flow import *

# get a logger
logger = logging.getLogger(__name__)


#######################################
### test the Authentication class ###
#######################################

# remove the TMPJSONFILE
def removeTMPJSONFILE():
    if os.path.exists(TMPJSONFILE):
        logger.debug("removing TMPJSONFILE '{}'".format(TMPJSONFILE))
        os.remove(TMPJSONFILE)

######################################
### Test JSON IO wrapper functions ###
######################################
class JSONioTest(BasicTest):
    # execute this before each test method
    def setUp(self):
        # make sure, there is no authfile in the beginning
        removeTMPJSONFILE()

    # execute this after each test method
    def tearDown(self):
        # make sure, there is no authfile in the end
        removeTMPJSONFILE()

    @testname("nonexistant file---")
    def test_ReadNonexistantFile(self):
        # result should be empty dict
        self.assertEqual(
            utils.read_json_from_file(TMPJSONFILE), utils.EMPTY_JSON)

    @testname("empty file")
    def test_ReadEmptyFile(self):
        # create empty file
        with open(TMPJSONFILE,"w"): pass
        # result should be empty dict
        self.assertEqual(
            utils.read_json_from_file(TMPJSONFILE), utils.EMPTY_JSON)

    @testname("invalid JSON file")
    def test_ReadInvalidJSONFile(self):
        # create invalid JSON file
        with open(TMPJSONFILE,"w") as f: 
            f.write("-_-\" This is definitely no JSON... #-*asdf*-#")
        # result should be empty dict
        self.assertEqual(
            utils.read_json_from_file(TMPJSONFILE), utils.EMPTY_JSON)

    @testname("write invalid JSON data")
    def test_WriteInvalidJSON(self):
        # try to write module 'json' (not JSON serializable) to file
        self.assertFalse(utils.write_json_to_file(json, TMPJSONFILE))
        # the file should NOT have been created
        self.assertFalse(os.path.exists(TMPJSONFILE))

    @testname("write/read valid JSON file")
    def test_WriteReadvalidJSONFile(self):
        # create valid JSON file, function should return True
        self.assertTrue(utils.write_json_to_file(EXAMPLE_JSON, TMPJSONFILE))
        # the file should have been created
        self.assertTrue(os.path.exists(TMPJSONFILE))
        # result should be the same JSON 
        self.assertEqual(utils.read_json_from_file(TMPJSONFILE), EXAMPLE_JSON)



def run():
    # run the tests
    logger.info("=== UTILS TESTS ===")
    unittest.main(exit=False,module=__name__)
    logger.info("=== END OF UTILS TESTS ===")
