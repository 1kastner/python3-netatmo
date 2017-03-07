#!/usr/bin/env python3
# system modules
import unittest
import logging
import os
import shutil
import json
import time
import http.client
import pandas

# import authentication module
from netatmo.api import authentication
# import client module
from netatmo.api import client
# import test data
from .test_data import *
from .test_flow import *

# test settings
OFFLINE = False # set to True to run only non-network tests

# skip everything
SKIPALL = False # by default, don't skip everything

# get a logger
logger = logging.getLogger(__name__)


#############################
### test the Client class ###
#############################

# remove the TMPAUTHFILE
def removeTMPAUTHFILE():
    if os.path.exists(TMPAUTHFILE):
        logger.debug("removing TPMAUTHFILE '{}'".format(TMPAUTHFILE))
        os.remove(TMPAUTHFILE)

# get the JSON content of TMPAUTHFILE
def TMPAUTHFILEjson():
    try: # open and read, return result
        with open(TMPAUTHFILE, "r") as f:
            return json.load(f)
    except: # didn't work, return empty dict
        return {}

##################################
### base class for ClientTests ###
##################################
class ClientTest(BasicTest):
    # execute this before each test method
    def setUp(self):
        # unset the client
        self.client = None
        # read user data
        self.user_data = read_json_from_file(USER_DATA_JSONFILE)
        # make sure, there is no authfile in the beginning
        removeTMPAUTHFILE()

    # execute this after each test method
    def tearDown(self):
        # unset the client 
        self.client = None
        # unset the user credentials
        self.user_data = None
        # make sure, there is no authfile in the end
        removeTMPAUTHFILE()

    # check if Client object has all needed properties
    def client_has_all_needed_properties(self):
        # property classes
        types = {
            "authentication": authentication.Authentication,
        }
        # check for existence of properties
        # hasattr(self.client,prop) is not suitable because of the
        # (hasattr calls the property's getter somehow)
        for prop, cls in types.items():
            self.assertTrue(prop in dir(self.client))
            # Check that client.prop has correct class
            self.assertIsInstance(getattr(self.client,prop), cls)


####################################################
### test the different Client construction cases ###
####################################################
class ClientConstructorTest(ClientTest):
    # empty constructor test
    @testname("empty constructor")
    @unittest.skipIf(SKIPALL,"skipping all tests")
    def test_Empty(self):
        # initialize without any arguments
        self.client = client.NetatmoClient()
        # check properties
        self.client_has_all_needed_properties()

    @testname("constructor with authentication")
    @unittest.skipIf(SKIPALL,"skipping all tests")
    def test_OnlyEmptyAuthentication(self):
        # an authentication
        auth = authentication.Authentication()
        # initialize only with authentication
        self.client = client.NetatmoClient(authentication = auth)
        # attribute should be the same
        self.assertEqual(self.client.authentication, auth)
        
##########################################
### test the different Client requests ###
##########################################
class ClientRequestsTest(ClientTest):
    def setUp(self):
        # read user data
        self.user_data = read_json_from_file(USER_DATA_JSONFILE)
        REAL_CREDENTIALS = self.user_data.get("credentials")
        if not REAL_CREDENTIALS: self.skipTest("user credentials missing " 
            "in {}".format(USER_DATA_JSONFILE))
        # an authentication
        auth = authentication.Authentication()
        auth.credentials = REAL_CREDENTIALS
        auth.tmpfile = TMPAUTHFILE
        # a client
        self.client = client.NetatmoClient(authentication = auth)

    # execute this after each test method
    def tearDown(self):
        # unset the client 
        self.client = None
        # unset the user credentials
        self.user_data = None

    @classmethod
    def setUpClass(cls):
        # make sure, there is no authfile in the beginning
        removeTMPAUTHFILE()

    @classmethod
    def tearDownClass(cls):
        # make sure, there is no authfile in the end
        removeTMPAUTHFILE()
        
    # getpublicdata with correct region
    @testname("Getpublicdata with correct region")
    @unittest.skipIf(SKIPALL,"skipping all tests")
    def test_GetpublicdataWithHamburgRegion(self):
        if OFFLINE: self.skipTest("skip network dependant tests")
        # request with only hamburg coordinates
        res = self.client.Getpublicdata(region = HAMBURG_COORDINATES_OUTLINE)
        # check converted response class
        self.assertIsInstance(res.dataframe,pandas.DataFrame)
    
    # getmeasure with correct data
    @testname("Getmeasure with correct data and only device_id")
    @unittest.skipIf(SKIPALL,"skipping all tests")
    def test_GetmeasureWithETADevice(self):
        if OFFLINE: self.skipTest("skip network dependant tests")
        DEVICE_ID = self.user_data.get("device",{}).get("device_id")
        if not DEVICE_ID: self.skipTest("user device id missing " 
            "in {}".format(USER_DATA_JSONFILE))
        # request 
        res = self.client.Getmeasure( 
            device_id = DEVICE_ID,
            optimize = False
            )
        # check converted response class
        self.assertIsInstance(res.dataframe,pandas.DataFrame)

    # getmeasure with correct data
    @testname("Getmeasure with correct data and device_id and module_id")
    @unittest.skipIf(SKIPALL,"skipping all tests")
    def test_GetmeasureWithETADeviceAndModule(self):
        if OFFLINE: self.skipTest("skip network dependant tests")
        DEVICE_ID = self.user_data.get("device",{}).get("device_id")
        if not DEVICE_ID: self.skipTest("user device id missing " 
            "in {}".format(USER_DATA_JSONFILE))
        MODULE_ID = self.user_data.get("device",{}).get("module_id")
        if not MODULE_ID: self.skipTest("user module id missing " 
            "in {}".format(USER_DATA_JSONFILE))
        # request 
        res = self.client.Getmeasure( 
            device_id = DEVICE_ID,
            module_id = MODULE_ID,
            optimize = False
            )
        # check converted response class
        self.assertIsInstance(res.dataframe,pandas.DataFrame)

    # getmeasure with correct data
    @testname("Getstationsdata with correct data")
    @unittest.skipIf(SKIPALL,"skipping all tests")
    def test_GetstationsdataWithDevice(self):
        if OFFLINE: self.skipTest("skip network dependant tests")
        DEVICE_ID = self.user_data.get("device",{}).get("device_id")
        if not DEVICE_ID: self.skipTest("user device id missing " 
            "in {}".format(USER_DATA_JSONFILE))
        # request with only hamburg coordinates
        res = self.client.Getstationsdata( 
            device_id = DEVICE_ID,
            )
        # check converted response class
        self.assertIsInstance(res.dataframe,pandas.DataFrame)

        


def run():
    # run the tests
    logger.info("=== CLIENT TESTS ===")
    unittest.main(exit=False,module=__name__)
    logger.info("=== END OF CLIENT TESTS ===")
