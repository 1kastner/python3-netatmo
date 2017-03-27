#!/usr/bin/env make -f

SETUP.PY = ./setup.py
INIT.PY = $(shell find netatmo -maxdepth 1 -type f -name '__init__.py')

VERSION = $(shell perl -ne 'if (s/^.*__version__\s*=\s*"(\d+\.\d+.\d+)".*$$/$$1/g){print;exit}' $(INIT.PY))

.PHONY: all
all: wheel

.PHONY: build
build: 
	$(SETUP.PY) build

.PHONY: wheel
wheel:
	$(SETUP.PY) sdist bdist_wheel

.PHONY: upload
upload: wheel tag
	$(SETUP.PY) sdist upload -r pypi

.PHONY: upload-test
upload-test: wheel tag
	$(SETUP.PY) sdist upload -r pypitest

.PHONY: increase-patch
increase-patch: $(INIT.PY)
	perl -pi -e 's/(__version__\s*=\s*")(\d+)\.(\d+).(\d+)(")/$$1.(join ".",$$2,$$3,$$4+1).$$5/ge' $(INIT.PY)

.PHONY: increase-minor
increase-minor: $(INIT.PY)
	perl -pi -e 's/(__version__\s*=\s*")(\d+)\.(\d+).(\d+)(")/$$1.(join ".",$$2,$$3+1,0).$$5/ge' $(INIT.PY)

.PHONY: increase-major
increase-major: $(INIT.PY)
	perl -pi -e 's/(__version__\s*=\s*")(\d+)\.(\d+).(\d+)(")/$$1.(join ".",$$2+1,0,0).$$5/ge' $(INIT.PY)

.PHONY: tag
tag:
	git tag -f v$(VERSION)

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


.PHONY: clean
clean:

.PHONY: distclean
distclean: clean
	rm -rf *.egg-info
	rm -rf build
	rm -rf $$(find -type d -iname __pycache__)
	rm -f $$(find -type f -iname '*.pyc')