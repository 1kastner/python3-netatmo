#!/usr/bin/env make -f

SETUP.CFG = ./setup.cfg
SETUP.CFG.BAK = ./setup.cfg.bak

SETUP.PY = ./setup.py

SETUP.CFG.VERSION = $(shell perl -ne 'if(s/^\s*version\s*=\s*(\d+\.\d+\.\d+).*$$/$$1/g){print;exit}' $(SETUP.CFG))

NETATMO_INIT.PY = ./netatmo/__init__.py


.PHONY: all
all: build

.PHONY: build
build: $(NETATMO_INIT.PY)
	$(SETUP.PY) build

# update the version string in the code
$(NETATMO_INIT.PY): $(SETUP.CFG)
	perl -pi -e 's/^(__version__\s*=\s*)("[^"]+")$$/$$1"$(SETUP.CFG.VERSION)"/g' $(NETATMO_INIT.PY)
	
.PHONY: increase-patch
increase-patch: $(SETUP.CFG) $(SETUP.CFG.BAK)
	perl6 -p -e 's:s:g/("version"\h*"="\h*)(\d+)\.(\d+).(\d+)/{$$0}$$1\.$$2\.{$$3+1}/' < $(SETUP.CFG.BAK) > $(SETUP.CFG)
	$(MAKE) $(NETATMO_INIT.PY)

.PHONY: increase-minor
increase-minor: $(SETUP.CFG) $(SETUP.CFG.BAK)
	perl6 -p -e 's:s:g/("version"\h*"="\h*)(\d+)\.(\d+).(\d+)/{$$0}$$1\.{$$2+1}\.0/' < $(SETUP.CFG.BAK) > $(SETUP.CFG)
	$(MAKE) $(NETATMO_INIT.PY)

.PHONY: increase-major
increase-major: $(SETUP.CFG) $(SETUP.CFG.BAK)
	perl6 -p -e 's:s:g/("version"\h*"="\h*)(\d+)\.(\d+).(\d+)/{$$0}{$$1+1}\.0\.0/' < $(SETUP.CFG.BAK) > $(SETUP.CFG)
	$(MAKE) $(NETATMO_INIT.PY)

$(SETUP.CFG.BAK): $(SETUP.CFG)
	cp $(SETUP.CFG) $(SETUP.CFG.BAK)

.PHONY: clean
clean:
	rm -f $(SETUP.CFG.BAK)

.PHONY: distclean
distclean: clean
	rm -rf *.egg-info
	rm -rf build
	rm -rf $$(find -type d -iname __pycache__)
	rm -f $$(find -type f -iname '*.pyc')

.PHONY: setup-test
setup-test:
	$(SETUP.PY) test
	
.PHONY: test
test:
	python3 -c 'import tests;tests.runall(verbose=False,offline=False)'

.PHONY: testverbose
testverbose:
	python3 -c 'import tests;tests.runall(verbose=True,offline=False)'

.PHONY: testoffline
testoffline:
	python3 -c 'import tests;tests.runall(verbose=False,offline=True)'

.PHONY: testofflineverbose
testofflineverbose:
	python3 -c 'import tests;tests.runall(verbose=True,offline=True)'

.PHONY: testauth
testauth:
	python3 -c 'import tests;tests.runtest(module=tests.authentication,verbose=False,offline=False)'

.PHONY: testauthverbose
testauthverbose:
	python3 -c 'import tests;tests.runtest(module=tests.authentication,verbose=True,offline=False)'

.PHONY: testauthoffline
testauthoffline:
	python3 -c 'import tests;tests.runtest(module=tests.authentication,verbose=False,offline=True)'

.PHONY: testauthofflineverbose
testauthofflineverbose:
	python3 -c 'import tests;tests.runtest(module=tests.authentication,verbose=True,offline=True)'

.PHONY: testclient
testclient:
	python3 -c 'import tests;tests.runtest(module=tests.client,verbose=False,offline=False)'

.PHONY: testclientverbose
testclientverbose:
	python3 -c 'import tests;tests.runtest(module=tests.client,verbose=True,offline=False)'

.PHONY: testclientoffline
testclientoffline:
	python3 -c 'import tests;tests.runtest(module=tests.client,verbose=False,offline=True)'

.PHONY: testclientofflineverbose
testclientofflineverbose:
	python3 -c 'import tests;tests.runtest(module=tests.client,verbose=True,offline=True)'
