#!/usr/bin/env python3
# system modules
import unittest
import logging
import os
import shutil
import json
import time

# import authentication module
from netatmo.api import authentication
# import test data
from .test_data import *
from .test_flow import *

# test settings
OFFLINE = False # set to True to run only non-network tests

# skip everything
SKIPALL = False # by default, don't skip everything

# get a logger
logger = logging.getLogger(__name__)


#######################################
### test the Authentication class ###
#######################################

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

############################################
### base class for AuthenticationTests ###
############################################
class AuthenticationTest(BasicTest):
    # execute this before each test method
    def setUp(self):
        # unset the auth
        self.auth = None
        # read user data
        self.user_data = read_json_from_file(USER_DATA_JSONFILE)
        # make sure, there is no authfile in the beginning
        removeTMPAUTHFILE()

    # execute this after each test method
    def tearDown(self):
        # unset the auth
        self.auth = None
        # unset the user credentials
        self.user_data = None
        # make sure, there is no authfile in the end
        removeTMPAUTHFILE()

    # check if Authentication object has all needed properties
    def auth_has_all_needed_properties(self):
        # check for existence of properties
        # hasattr(self.auth,prop) is not suitable because of the
        # Authentication's automatic update magic
        # (hasattr calls the property's getter somehow)
        for prop in ["tokens","credentials","tmpfile"]:
            self.assertTrue(prop in dir(self.auth))


##############################################################
### test the different Authentication construction cases ###
##############################################################
class AuthenticationConstructorTest(AuthenticationTest):
    # empty constructor test
    @testname("empty constructor")
    @unittest.skipIf(SKIPALL,"skipping all tests")
    def test_Empty(self):
        # initialize without any arguments
        self.auth = authentication.Authentication()
        # check properties
        self.auth_has_all_needed_properties()
        # tokens should be empty template
        self.assertEqual(self.auth.tokens, authentication.EMPTY_TOKENS)
        # credentials should be empty template
        self.assertEqual(
            self.auth.credentials, authentication.EMPTY_CREDENTIALS)
        # tmpfile should be None
        self.assertEqual(self.auth.tmpfile,None)
        # check that no auth tmpfile was created
        self.assertFalse(os.path.exists(TMPAUTHFILE))

    # constructor with only nonexistant file given
    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("only nonexistant tmpfile given in constructor")
    def test_OnlyNonexistantTmpfile(self):
        # initialize with tmpfile
        self.auth = authentication.Authentication(tmpfile = TMPAUTHFILE)
        # check properties
        self.auth_has_all_needed_properties()
        # tokens should be empty template
        self.assertEqual(self.auth.tokens, authentication.EMPTY_TOKENS)
        # credentials should be empty template
        self.assertEqual(
            self.auth.credentials, authentication.EMPTY_CREDENTIALS)
        # tmpfile should be set to the TMPAUTHFILE
        self.assertEqual(self.auth.tmpfile,TMPAUTHFILE)
        # check that an auth tmpfile was created
        self.assertTrue(os.path.exists(TMPAUTHFILE))
        # check that EMPTY_TOKENS are automatically written to auth tmpfile
        self.assertEqual(TMPAUTHFILEjson(), authentication.EMPTY_TOKENS)

    # constructor with only existant but empty file given
    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("only existant but empty tmpfile given in constructor")
    def test_OnlyEmptyTmpfile(self):
        # create empty TMPAUTHFILE
        with open(TMPAUTHFILE,"w"): pass
        # initialize with tmpfile
        self.auth = authentication.Authentication(tmpfile = TMPAUTHFILE)
        # check properties
        self.auth_has_all_needed_properties()
        # tokens should be empty template
        self.assertEqual(self.auth.tokens, authentication.EMPTY_TOKENS)
        # credentials should be empty template
        self.assertEqual(
            self.auth.credentials, authentication.EMPTY_CREDENTIALS)
        # tmpfile should be set to the TMPAUTHFILE
        self.assertEqual(self.auth.tmpfile,TMPAUTHFILE)
        # check that EMPTY_TOKENS are automatically written to auth tmpfile
        self.assertEqual(TMPAUTHFILEjson(), authentication.EMPTY_TOKENS)

    # constructor with only existant but empty file given
    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("only existant but non-JSON tmpfile given in constructor")
    def test_OnlyNonJSONtmpfile(self):
        # create TMPAUTHFILE with Non-JSON content
        with open(TMPAUTHFILE,"w") as f: 
            f.write("-_-\" This is definitely no JSON... #-*asdf*-#")
        # initialize with tmpfile
        self.auth = authentication.Authentication(tmpfile = TMPAUTHFILE)
        # check properties
        self.auth_has_all_needed_properties()
        # tokens should be empty template
        self.assertEqual(self.auth.tokens, authentication.EMPTY_TOKENS)
        # credentials should be empty template
        self.assertEqual(
            self.auth.credentials, authentication.EMPTY_CREDENTIALS)
        # tmpfile should be set to the TMPAUTHFILE
        self.assertEqual(self.auth.tmpfile,TMPAUTHFILE)
        # check that EMPTY_TOKENS are automatically written to auth tmpfile
        self.assertEqual(TMPAUTHFILEjson(), authentication.EMPTY_TOKENS)

    # constructor with only existant but incomplete tmpfile given
    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("only incomplete tokens in JSON tmpfile given in constructor")
    def test_OnlyIncompleteJSONtmpfile(self):
        incomplete_tokens = EXAMPLE_TOKENS.copy() # a copy of the examples
        incomplete_tokens.pop("access_token") # remove the access token
        # create TMPAUTHFILE with incomplete tokens
        with open(TMPAUTHFILE,"w") as f: # open file
            json.dump(incomplete_tokens, f) # write incomplete tokens to file
        # initialize with incomplete tmpfile
        try:
            self.auth = authentication.Authentication(tmpfile = TMPAUTHFILE)
        except AssertionError:
            # The authentication is supposed to fail here, because this
            # is a user error. This class does only writeout full token datasets
            # (that are possibly empty), but never incomplete sets.
            pass

    # constructor with only existant but non-json file given
    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("only minimal JSON tmpfile given in constructor")
    def test_OnlyMinimalJSONtmpfile(self):
        # create TMPAUTHFILE with Non-JSON content
        with open(TMPAUTHFILE,"w") as f: 
            json.dump(EXAMPLE_TOKENS,f)
        # initialize with tmpfile
        self.auth = authentication.Authentication(tmpfile = TMPAUTHFILE)
        # check properties
        self.auth_has_all_needed_properties()
        # tokens should be the tokens from the file template
        self.assertEqual(self.auth.tokens, EXAMPLE_TOKENS)
        # credentials should be empty template
        self.assertEqual(
            self.auth.credentials, authentication.EMPTY_CREDENTIALS)
        # tmpfile should be set to the TMPAUTHFILE
        self.assertEqual(self.auth.tmpfile,TMPAUTHFILE)
        # check that the EXAMPLE_TOKENS are left unchanged in the tmpfile
        self.assertEqual(TMPAUTHFILEjson(), EXAMPLE_TOKENS)

    # constructor with only invalid credentials
    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("only invalid credentials in constructor")
    def test_OnlyInvalidCredentials(self):
        # initialize without any arguments
        invalid_credentials = {"bla":"blubb"}
        try:
            self.auth = authentication.Authentication(
                credentials = invalid_credentials)
        except AssertionError:
            # This is a user error, the class should fail here.
            pass

    # constructor with only full credentials
    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("only full credentials in constructor")
    def test_OnlyFullRealCredentials(self):
        REAL_CREDENTIALS = self.user_data.get("credentials")
        if not REAL_CREDENTIALS: self.skipTest("user credentials missing " 
            "in {}".format(USER_DATA_JSONFILE))
        # initialize without any arguments
        self.auth = authentication.Authentication(
            credentials = REAL_CREDENTIALS)
        # check properties
        self.auth_has_all_needed_properties()
        # credentials should be empty template
        self.assertEqual(self.auth.credentials, REAL_CREDENTIALS)
        # tokens should be fetched automatically
        self.assertFalse(self.auth.tokens_defined)
        self.assertFalse(self.auth.tokens_are_up_to_date)
        # tmpfile should be None
        self.assertEqual(self.auth.tmpfile,None)
        # check that no auth tmpfile was created
        self.assertFalse(os.path.exists(TMPAUTHFILE))

    # constructor with only invalid tokens given
    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("only invalid tokens in constructor")
    def test_OnlyInvalidTokens(self):
        for invalid_tokens in ["a",{"a":"b"}]:
            self.auth = authentication.Authentication(
                tokens = invalid_tokens)
            logger.info("use only invalid tokens '{}' in constructor".format(
                invalid_tokens))
            # check properties
            self.auth_has_all_needed_properties()
            # tokens should be empty template
            self.assertEqual(self.auth.tokens, authentication.EMPTY_TOKENS)
            # credentials should be empty template
            self.assertEqual(self.auth.credentials, 
                authentication.EMPTY_CREDENTIALS)
            # tmpfile should be None
            self.assertEqual(self.auth.tmpfile,None)
            # check that no auth tmpfile was created
            self.assertFalse(os.path.exists(TMPAUTHFILE))
        
    # constructor with only valid tokens given
    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("only valid tokens in constructor")
    def test_OnlyValidTokens(self):
        example_tokens = EXAMPLE_TOKENS.copy()
        self.auth = authentication.Authentication(
            tokens = example_tokens # hand in example tokens
            )
        # check properties
        self.auth_has_all_needed_properties()
        # tokens should be example tokens
        self.assertEqual(self.auth.tokens, example_tokens)
        # credentials should be empty template
        self.assertEqual(self.auth.credentials, 
            authentication.EMPTY_CREDENTIALS)
        # tmpfile should be None
        self.assertEqual(self.auth.tmpfile,None)
        # check that no auth tmpfile was created
        self.assertFalse(os.path.exists(TMPAUTHFILE))

    # constructor with valid tokens and tmpfile given
    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("valid tokens and nonexistant tmpfile in constructor")
    def test_ValidTokensAndNonexistantTmpfile(self):
        # initialize
        example_tokens = EXAMPLE_TOKENS.copy()
        self.auth = authentication.Authentication(
            tokens  = example_tokens, # hand in example tokens
            tmpfile = TMPAUTHFILE     # hand in a nonexistant tmpfile
            )
        # check properties
        self.auth_has_all_needed_properties()
        # tokens should be empty template
        self.assertEqual(self.auth.tokens, example_tokens)
        # credentials should be empty template
        self.assertEqual(self.auth.credentials, 
            authentication.EMPTY_CREDENTIALS)
        # tmpfile should be set
        self.assertEqual(self.auth.tmpfile,TMPAUTHFILE)
        # check that the auth tmpfile was created
        self.assertTrue(os.path.exists(TMPAUTHFILE))

    # constructor with valid tokens and existant tmpfile given
    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("valid tokens and existant but empty tmpfile in constructor")
    def test_ValidTokensAndEmptyTmpfile(self):
        # create empty TMPAUTHFILE
        with open(TMPAUTHFILE,"w"): pass
        # initialize
        example_tokens = EXAMPLE_TOKENS.copy()
        self.auth = authentication.Authentication(
            tokens  = example_tokens, # hand in example tokens
            tmpfile = TMPAUTHFILE     # hand in a nonexistant tmpfile
            )
        # check properties
        self.auth_has_all_needed_properties()
        # tokens should be empty template
        self.assertEqual(self.auth.tokens, example_tokens)
        # credentials should be empty template
        self.assertEqual(self.auth.credentials, 
            authentication.EMPTY_CREDENTIALS)
        # tmpfile should be set
        self.assertEqual(self.auth.tmpfile,TMPAUTHFILE)
        # check that the auth tmpfile was created
        self.assertTrue(os.path.exists(TMPAUTHFILE))
        # check that the initialized tokens are written to the tmpfile
        self.assertEqual(TMPAUTHFILEjson(), EXAMPLE_TOKENS)

    # constructor with valid tokens and valid token json tmpfile given
    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("valid tokens and valid JSON tokens tmpfile in constructor")
    def test_ValidTokensAndValidJSONTmpfile(self):
        file_tokens = EXAMPLE_TOKENS.copy()
        # create valid TMPAUTHFILE
        with open(TMPAUTHFILE,"w") as f: json.dump(file_tokens, f)
        # initialize
        constructor_tokens = EXAMPLE_TOKENS_2.copy()
        self.auth = authentication.Authentication(
            tokens  = constructor_tokens, # hand in OTHER tokens than in tmpfile
            tmpfile = TMPAUTHFILE         # hand in a nonexistant tmpfile
            )
        # check properties
        self.auth_has_all_needed_properties()
        # tokens should be given tokens
        self.assertEqual(self.auth.tokens, constructor_tokens)
        # credentials should be empty template
        self.assertEqual(self.auth.credentials, 
            authentication.EMPTY_CREDENTIALS)
        # tmpfile should be set
        self.assertEqual(self.auth.tmpfile,TMPAUTHFILE)
        # check that the auth tmpfile was created
        self.assertTrue(os.path.exists(TMPAUTHFILE))
        # check that the initialized tokens are (over)written into the tmpfile
        self.assertEqual(TMPAUTHFILEjson(), constructor_tokens)

    # constructor with valid credentials and nonexistant tmpfile
    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("valid credentials and nonexistant tmpfile in constructor")
    def test_ValidCredentialsAndNonexistantTmpfile(self):
        if OFFLINE: self.skipTest("skip network dependant tests")
        REAL_CREDENTIALS = self.user_data.get("credentials")
        if not REAL_CREDENTIALS: self.skipTest("user credentials missing " 
            "in {}".format(USER_DATA_JSONFILE))
        # initialize
        self.auth = authentication.Authentication(
            credentials = REAL_CREDENTIALS, # real credentials
            tmpfile = TMPAUTHFILE           # hand in a nonexistant tmpfile
            )
        # check properties
        self.auth_has_all_needed_properties()
        # tokens should be given tokens
        self.assertEqual(self.auth.credentials, REAL_CREDENTIALS)
        # tmpfile should be set
        self.assertEqual(self.auth.tmpfile,TMPAUTHFILE)
        # check that the auth tmpfile was created
        self.assertTrue(os.path.exists(TMPAUTHFILE))
        # check that the initialized tokens are (over)written into the tmpfile
        self.assertEqual(TMPAUTHFILEjson(), authentication.EMPTY_TOKENS)

#############################################################################
### test the different Authentication interactive property change cases ###
#############################################################################
class AuthenticationInteractivePropertyChangeTest(AuthenticationTest):
    # execute this before each test method
    def setUp(self):
        # set auth to empty authentication
        self.auth = authentication.Authentication()
        # read user data
        self.user_data = read_json_from_file(USER_DATA_JSONFILE)
        # make sure, there is no authfile in the beginning
        removeTMPAUTHFILE()

    # execute this after each test method
    def tearDown(self):
        # unset the auth
        self.auth = None
        # unset the user credentials
        self.user_data = None
        # make sure, there is no authfile in the end
        removeTMPAUTHFILE()

    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("initialized without arguments, set tmpfile to nonexistant file")
    def test_setTmpfileToNonExistantFile(self):
        self.auth.tmpfile = TMPAUTHFILE # set to nonexistant file
        self.assertTrue(os.path.exists(TMPAUTHFILE)) # file should be created
        # empty tokens should automatically be written to file
        self.assertEqual(TMPAUTHFILEjson(), authentication.EMPTY_TOKENS)

    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("initialized without arguments, set tmpfile to empty file")
    def test_setTmpfileToEmptyFile(self):
        with open(TMPAUTHFILE,"w"): pass # create empty file
        self.auth.tmpfile = TMPAUTHFILE # set to nonexistant file
        # empty tokens should automatically be written to file
        self.assertEqual(TMPAUTHFILEjson(), authentication.EMPTY_TOKENS)

    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("initialized without arguments, set tmpfile to invalid file")
    def test_setTmpfileToExistantInvalidFile(self):
        with open(TMPAUTHFILE,"w") as f: # create invalid file
            f.write("-_-\" This is definitely no JSON... #-*asdf*-#")
        self.auth.tmpfile = TMPAUTHFILE # set to invalid file
        # empty tokens should automatically be written to file
        self.assertEqual(TMPAUTHFILEjson(), authentication.EMPTY_TOKENS)

    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("initialized without arguments, set tmpfile to valid file")
    def test_setTmpfileToExistantValidFile(self):
        with open(TMPAUTHFILE,"w") as f: # create valid file
            json.dump(EXAMPLE_TOKENS, f)
        self.auth.tmpfile = TMPAUTHFILE # set to valid file
        # new tokens should automatically be read from file
        self.assertEqual(self.auth.tokens, EXAMPLE_TOKENS)
        # file should have been left as-is
        self.assertEqual(TMPAUTHFILEjson(), EXAMPLE_TOKENS)

    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("initialized without arguments, set tokens to something invalid")
    def test_setTokensToInvalid(self):
        self.auth.tokens = {"a":"b"} # invalid new tokens
        # tokens should be set to empty default
        self.assertEqual(self.auth.tokens, authentication.EMPTY_TOKENS)

    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("initialized without arguments, set tokens to something valid")
    def test_setTokensToValid(self):
        self.auth.tokens = EXAMPLE_TOKENS.copy() # valid new tokens
        # tokens should be set to empty default
        self.assertEqual(self.auth.tokens, EXAMPLE_TOKENS)

    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("initialized without arguments, set tmpfile to nonexistant file, "
              "then tokens to something valid")
    def test_setTmpfileToNonexistantThenTokensToValid(self):
        self.auth.tmpfile = TMPAUTHFILE # set to nonexistant file
        self.auth.tokens = EXAMPLE_TOKENS.copy() # set valid new tokens
        # new tokens should have been written to file
        self.assertEqual(TMPAUTHFILEjson(), EXAMPLE_TOKENS)

    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("initialized without arguments, set tmpfile to valid file, "
              "then tokens to something valid")
    def test_setTmpfileToValidThenTokensToValid(self):
        with open(TMPAUTHFILE,"w") as f: # create valid file
            json.dump(EXAMPLE_TOKENS, f)
        self.auth.tmpfile = TMPAUTHFILE # set to nonexistant file
        self.auth.tokens = EXAMPLE_TOKENS_2.copy() # set valid new tokens
        # new tokens should have been written to file
        self.assertEqual(TMPAUTHFILEjson(), EXAMPLE_TOKENS_2)

    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("initialized without arguments, set credentials to sth. valid")
    def test_setCredentialsToValid(self):
        self.auth.credentials = EXAMPLE_CREDENTIALS # set to valid credentials
        # the property should have been set
        self.assertEqual(self.auth.credentials, EXAMPLE_CREDENTIALS)

    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("initialized without arguments, set credentials to sth. invalid")
    def test_setCredentialsToInvalid(self):
        try:
            self.auth.credentials = {"a":"b"} # set to invalid credentials
        except AssertionError:
            # Setting bogus credentials is a user error, thus it's okay
            # to raise an error here
            pass

######################################################################
### test the Authentication token requests property change cases ###
######################################################################
class AuthenticationTokenRequestsTest(AuthenticationTest):
    # execute this before each test method
    def setUp(self):
        # make sure, there is no authfile in the beginning
        removeTMPAUTHFILE()
        # initialize without arguments
        self.auth = authentication.Authentication()
        # read user data
        self.user_data = read_json_from_file(USER_DATA_JSONFILE)

    # execute this after each test method
    def tearDown(self):
        # unset the auth
        self.auth = None
        # unset the user credentials
        self.user_data = None
        # make sure, there is no authfile in the end
        removeTMPAUTHFILE()

    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("initialized without arguments, set credentials, " 
              "then do a new token request")
    def test_CredentialsNewTokenRequest(self):
        if OFFLINE: self.skipTest("skip network dependant tests")
        REAL_CREDENTIALS = self.user_data.get("credentials")
        if not REAL_CREDENTIALS: self.skipTest("user credentials missing " 
            "in {}".format(USER_DATA_JSONFILE))
        # set credentials
        self.auth.credentials = REAL_CREDENTIALS
        # do a new token request
        self.auth.request_new_tokens()
        # check that tokens now aren't empty anymore
        self.assertTrue(self.auth.tokens_defined)

    @testname("empty constructor, new tokens request, " 
              "then token refresh request, " 
              "tokens should be up to date")
    @unittest.skipIf(SKIPALL,"skipping all tests")
    def test_AfterNewTokensRequestAndRefreshRequest(self):
        if OFFLINE: self.skipTest("skip network dependant tests")
        REAL_CREDENTIALS = self.user_data.get("credentials")
        if not REAL_CREDENTIALS: self.skipTest("user credentials missing " 
            "in {}".format(USER_DATA_JSONFILE))
        # set credentials
        self.auth.credentials = REAL_CREDENTIALS
        # request new tokens
        self.auth.request_new_tokens()
        # request new tokens
        self.auth.refresh_current_tokens()
        # tokens should be up to date
        self.assertTrue(self.auth.tokens_are_up_to_date)

    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("initialized without arguments, set invalid credentials, "
              "then do a new token request")
    def test_InvalidCredentialsNewTokenRequest(self):
        if OFFLINE: self.skipTest("skip network dependant tests")
        # set credentials
        self.auth.credentials = EXAMPLE_CREDENTIALS
        try:
            # do a new token request
            self.auth.request_new_tokens()
        except authentication.InvalidCredentialsError:
            # This is a user error, there should be an Error here.
            pass

    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("initialized without arguments, set credentials, "
              "then set tmpfile to nonexistant file, "
              "then do a new token request")
    def test_CredentialsNonexistantTmpfileThenNewTokenRequest(self):
        if OFFLINE: self.skipTest("skip network dependant tests")
        REAL_CREDENTIALS = self.user_data.get("credentials")
        if not REAL_CREDENTIALS: self.skipTest("user credentials missing " 
            "in {}".format(USER_DATA_JSONFILE))
        # set credentials
        self.auth.credentials = REAL_CREDENTIALS
        # set tmpfile
        self.auth.tmpfile = TMPAUTHFILE
        # do a new token request
        self.auth.request_new_tokens()
        # check that tokens now aren't empty anymore
        self.assertTrue(self.auth.tokens_defined)
        # check that these tokens are written to the tmpfile
        self.assertEqual(self.auth.tokens, TMPAUTHFILEjson())
        # check that the request time was written to file
        self.assertTrue(
            abs(TMPAUTHFILEjson().get("token_request_time") - time.time()) < 5)

    @testname("initialized without arguments, set credentials, "
              "then do a new token request, then do a token refresh request")
    @unittest.skipIf(SKIPALL,"skipping all tests")
    def test_CredentialsNeTmpfileNewTokenRequestThenRefreshRequest(self):
        if OFFLINE: self.skipTest("skip network dependant tests")
        REAL_CREDENTIALS = self.user_data.get("credentials")
        if not REAL_CREDENTIALS: self.skipTest("user credentials missing " 
            "in {}".format(USER_DATA_JSONFILE))
        # set credentials
        self.auth.credentials = REAL_CREDENTIALS
        # set tmpfile
        self.auth.tmpfile = TMPAUTHFILE
        # do a new token request
        self.auth.request_new_tokens()
        access_token  = self.auth.tokens.get("access_token")
        refresh_token = self.auth.tokens.get("refresh_token")
        # do a token refresh request
        self.auth.refresh_current_tokens()
        # check that the tokens stayed the same
        self.assertEqual(access_token, self.auth.tokens.get("access_token"))
        self.assertEqual(refresh_token,self.auth.tokens.get("refresh_token"))
        # check that the refresh time was written to file
        self.assertTrue(
            abs(TMPAUTHFILEjson().get("refresh_request_time") - time.time())<5)


###################################################################
### test the automatic requesting functionality (theoretically) ###
###################################################################
class AuthenticationAutomaticRequestsTest(AuthenticationTest):
    # execute this before each test method
    def setUp(self):
        # initialize without arguments
        self.auth = authentication.Authentication()
        # read user data
        self.user_data = read_json_from_file(USER_DATA_JSONFILE)

    # execute this after each test method
    def tearDown(self):
        # unset the auth
        self.auth = None
        # unset the user credentials
        self.user_data = None

    @testname("empty constructor, tokens should be marked outdated")
    @unittest.skipIf(SKIPALL,"skipping all tests")
    def test_EmptyConstructor(self):
        # tokens should be outdated
        self.assertFalse(self.auth.tokens_are_up_to_date)

    @unittest.skipIf(SKIPALL,"skipping all tests")
    @testname("initialized without arguments, set credentials, " 
              "then access the token property. Tokens should be requested " 
              "automatically.")
    def test_RealCredentialsThenTokenGetter(self):
        if OFFLINE: self.skipTest("skip network dependant tests")
        REAL_CREDENTIALS = self.user_data.get("credentials")
        if not REAL_CREDENTIALS: self.skipTest("user credentials missing " 
            "in {}".format(USER_DATA_JSONFILE))
        # set credentials
        self.auth.credentials = REAL_CREDENTIALS
        # access the tokens property
        self.auth.tokens
        # check that tokens now aren't empty anymore
        self.assertTrue(self.auth.tokens_defined)
        self.assertTrue(self.auth.tokens_are_up_to_date)


    @testname("empty constructor, new tokens request, " 
              "then by hand set the request time way back," 
              "tokens should be outdated")
    @unittest.skipIf(SKIPALL,"skipping all tests")
    def test_AfterNewTokensRequestFakeOldRequestTime(self):
        if OFFLINE: self.skipTest("skip network dependant tests")
        REAL_CREDENTIALS = self.user_data.get("credentials")
        if not REAL_CREDENTIALS: self.skipTest("user credentials missing " 
            "in {}".format(USER_DATA_JSONFILE))
        # set credentials
        self.auth.credentials = REAL_CREDENTIALS
        # request new tokens
        self.auth.request_new_tokens()
        # by hand set the request time way back
        self.auth._tokens["token_request_time"] = time.time() - \
            authentication.DEFAULT_EXPIRE_TIME * 2
        # tokens should be outdated
        self.assertFalse(self.auth.tokens_are_up_to_date)

    @testname("empty constructor, new tokens request, then refresh request," 
              "then by hand set the request and refresh time way back," 
              "tokens should be outdated")
    @unittest.skipIf(SKIPALL,"skipping all tests")
    def test_AfterNewTokensRequestAndRefreshFakeOldRequestAndRefreshTime(self):
        if OFFLINE: self.skipTest("skip network dependant tests")
        REAL_CREDENTIALS = self.user_data.get("credentials")
        if not REAL_CREDENTIALS: self.skipTest("user credentials missing " 
            "in {}".format(USER_DATA_JSONFILE))
        # set credentials
        self.auth.credentials = REAL_CREDENTIALS
        # request new tokens
        self.auth.request_new_tokens()
        # request new tokens
        self.auth.refresh_current_tokens()
        # by hand set the request and refresh time way back
        self.auth._tokens["token_request_time"] = time.time() - \
            authentication.DEFAULT_EXPIRE_TIME - 100
        self.auth._tokens["token_refresh_time"] = time.time() - \
            authentication.DEFAULT_EXPIRE_TIME - 50
        # tokens should be outdated
        self.assertFalse(self.auth.tokens_are_up_to_date)


def run():
    # run the tests
    logger.info("=== AUTHENTICATION TESTS ===")
    unittest.main(exit=False,module=__name__)
    logger.info("=== END OF AUTHENTICATION TESTS ===")
