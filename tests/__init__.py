# -*- coding: utf-8 -*-
# System modules
import logging
import os

# External modules

# Internal modules

from . import authentication
from . import client
from . import utils

from . import test_data
from . import test_flow

__all__ = ['authentication','client','utils']

def runtest(module, verbose=False, offline=False):
    if verbose:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(filename=os.devnull) # discard any logging output
        # logging.basicConfig(level = logging.INFO)
    # run the tests
    try: 
        if offline: module.OFFLINE = True
    except: 
        pass
    module.run()

# run all tests
def runall(verbose=False, offline=False):
    for module in [authentication,client,utils]:
        runtest(module=module,verbose=verbose,offline=offline)
        print()

