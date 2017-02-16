#!/usr/bin/env python3
# System modules
import os

# External modules

# Internal modules

#######################################
### Constants and example test data ###
#######################################


#########################
### files and folders ###
#########################
TMPDIR = "TESTS_TMP"
# temporary json file
TMPJSONFILENAME = "test.json"
TMPJSONFILE = os.path.join(TMPDIR,TMPJSONFILENAME) 
# temporary authentication json file
TMPAUTHFILENAME = "authentication_test.json"
TMPAUTHFILE = os.path.join(TMPDIR,TMPAUTHFILENAME) 
# user data file
USER_DATA_JSONFILENAME = "USER_DATA.json"
USER_DATA_JSONFILE = os.path.join(os.path.dirname(__file__),
    USER_DATA_JSONFILENAME) 

#########################
### example JSON data ###
#########################
EXAMPLE_JSON = {
    "string":"foobar",
    "listofints":[1,2,3,4,5],
    "listofstr":["one","two","three"],
    "dict": {"key1":"value1","key2":"value2"}
}

#####################################
### example authentication data ###
#####################################
EXAMPLE_TOKENS = {
"refresh_token": "5829be1da467a393248b7533|6ff3e3c34569ff65cf0fff5e9b661a13", 
"access_token":  "5829be1da467a393248b7533|d7d5cfde48b936413ea851f893ba05af"
}

EXAMPLE_TOKENS_2 = {
"refresh_token": "6a48b7533ff3e5cfde48b693|643c34569ff65cf0fff5e9b661a13533", 
"access_token":  "ad31be1da467a3932488296b|7ed13ea851f893ba051da47be1db73af"
}

EXAMPLE_CREDENTIALS = {
    "password":"5uP3rP45sW0rD",
    "username":"user.email@internet.com",
    "client_id":    "03012823b3fd2e420fbf980b",
    "client_secret":"YXNkZmFzZGYgamFzamYgbGFzIG"
}

###########################
### example coordinates ###
###########################
HAMBURG_COORDINATES_OUTLINE = {
    "lat_ne" : 53.7499,
    "lat_sw" : 53.3809,
    "lon_ne" : 10.3471,
    "lon_sw" : 9.7085,
}

