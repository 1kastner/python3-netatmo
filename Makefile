#!/usr/bin/env make -f

SETUP.PY = ./setup.py
PACKAGE_FOLDER = netatmo
DOCS_FOLDER = docs
DOCS_API_FOLDER = docs/source/api
INIT.PY = $(shell find $(PACKAGE_FOLDER) -maxdepth 1 -type f -name '__init__.py')
RST_SOURCES = $(shell find $(DOCS_FOLDER) -type f -iname '*.rst')
PYTHON_SOURCES = $(shell find $(PACKAGE_FOLDER) -type f -iname '*.py')


VERSION = $(shell perl -ne 'if (s/^.*__version__\s*=\s*"(\d+\.\d+.\d+)".*$$/$$1/g){print;exit}' $(INIT.PY))

.PHONY: all
all: wheel docs

docs: $(PYTHON_SOURCES) $(RST_SOURCES)
	sphinx-apidoc -M -f -o $(DOCS_API_FOLDER) $(PACKAGE_FOLDER)
	cd $(DOCS_FOLDER) && make html

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
clean: distclean

.PHONY: distclean
distclean: clean
	rm -rf *.egg-info
	rm -rf build
	rm -rf $$(find -type d -iname '__pycache__')
	rm -f $$(find -type f -iname '*.pyc')
	(cd $(DOCS_FOLDER) && make clean)

.PHONY: travis-test
travis-test: wheel docs setup-test
