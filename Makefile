.PHONY:clean venv test coverage lint format deploy
all:clean test coverage lint

MIN_TEST_COVERAGE=99
INITIAL_PYTHON?=python3
VENV_DIR?=.venv
LIBRARY=devopsdriver
VENV_PYTHON?=$(VENV_DIR)/bin/python
VENV_PIP?=$(VENV_DIR)/bin/pip
SET_ENV?=. $(VENV_DIR)/bin/activate
SOURCES=$(shell find $(LIBRARY) -type f -iname "*.py")
TESTS=$(shell find tests -type f -iname "test_*.py")
FORMAT_FILE=$(VENV_DIR)/format.txt
LINT_FILE=$(VENV_DIR)/lint.txt
COVERAGE_FILE=.coverage
INFRASTRUCTURE=requirements-infrastructure.txt
INSTALL_INFRASTRUCTURE=$(VENV_PIP) install -q -r $(INFRASTRUCTURE)
DEPLOY_FILE=$(VENV_DIR)/deploy.txt
PROJECT_FILE=pyproject.toml
SLEEP_TIME_IN_SECONDS=30

$(VENV_DIR)/touchfile: $(PROJECT_FILE)
	@test -d $(VENV_DIR) || $(INITIAL_PYTHON) -m venv $(VENV_DIR)
	@echo Ensuring pip is latest version
	@$(SET_ENV); $(VENV_PIP) install --quiet --upgrade pip
	@echo Fetching requirements
	@$(SET_ENV); $(VENV_PIP) install --quiet --upgrade .
	@touch $@

venv: $(VENV_DIR)/touchfile

$(COVERAGE_FILE): $(VENV_DIR)/touchfile $(SOURCES) $(TESTS)
	@$(SET_ENV); $(INSTALL_INFRASTRUCTURE)
	@$(SET_ENV); $(VENV_PYTHON) -m coverage run  --source $(LIBRARY) -m pytest

test: $(COVERAGE_FILE)

coverage: $(COVERAGE_FILE)
	@$(SET_ENV); $(VENV_PYTHON) -m coverage report -m --sort=cover --skip-covered --fail-under=$(MIN_TEST_COVERAGE)
	@if grep -q "test+coverage&message=$(MIN_TEST_COVERAGE)%" README.md; then true; else echo "Update README.md test coverage" && false; fi
	

$(FORMAT_FILE): $(VENV_DIR)/touchfile $(SOURCES)
	@$(SET_ENV); $(INSTALL_INFRASTRUCTURE)
	@$(SET_ENV); $(VENV_PYTHON) -m black $(LIBRARY) &> $@

format: $(FORMAT_FILE)
	@cat $^

$(LINT_FILE): $(VENV_DIR)/touchfile $(SOURCES)
	@$(SET_ENV); $(INSTALL_INFRASTRUCTURE)
	-@$(SET_ENV); $(VENV_PYTHON) -m pylint $(LIBRARY) &> $@
	-@$(SET_ENV); $(VENV_PYTHON) -m black $(LIBRARY) --check >> $@  2>&1

lint: $(LINT_FILE)
	@cat $^

$(DEPLOY_FILE):$(LINT_FILE) $(COVERAGE_FILE) $(PROJECT_FILE) $(SOURCES) lint coverage
	@rm -Rf dist build *.egg-info $(VENV_DIR)/test_published
	@$(SET_ENV); \
		VERSION=`python -c "print(__import__('devopsdriver').__version__)"`; \
		if grep -q "released&message=v$$VERSION&" README.md; then true; else echo "Update README.md badge version" && false; fi
	@$(SET_ENV); \
		VERSION=`python -c "print(__import__('devopsdriver').__version__)"`; \
		if grep -q "devopsdriver/$$VERSION/" README.md; then true; else echo "Update README.md PyPI version" && false; fi
	@mkdir -p $(VENV_DIR)/test_published
	@$(SET_ENV); pip install build twine --upgrade
	@$(SET_ENV); $(VENV_PYTHON) -m build
	@$(SET_ENV); \
		REPO=`$(VENV_PYTHON) -m devopsdriver.settings pypi_test.repo`; \
		USERNAME=`$(VENV_PYTHON) -m devopsdriver.settings pypi_test.username`; \
		PASSWORD=`$(VENV_PYTHON) -m devopsdriver.settings pypi_test.password`; \
		$(VENV_PYTHON) -m twine upload --repository $$REPO dist/* --username $$USERNAME --password $$PASSWORD
	@echo Waiting for uploaded package to be avilable before testing
	@sleep $(SLEEP_TIME_IN_SECONDS)
	-@$(SET_ENV); \
		TESTURL=`$(VENV_PYTHON) -m devopsdriver.settings pypi_test.url`; \
		URL=`$(VENV_PYTHON) -m devopsdriver.settings pypi_prod.url`; \
		VERSION=`python -c "print(__import__('devopsdriver').__version__)"`; \
		cd $(VENV_DIR)/test_published; \
		$(INITIAL_PYTHON) -m venv .venv; \
		$(SET_ENV); \
		pip install --no-cache-dir --log $@ -i $$TESTURL  $(LIBRARY)==$$VERSION --extra-index-url $$URL; \
		$(VENV_PYTHON) -m devopsdriver.settings pypi_test.repo
	@$(SET_ENV); \
		TESTURL=`$(VENV_PYTHON) -m devopsdriver.settings pypi_test.url`; \
		URL=`$(VENV_PYTHON) -m devopsdriver.settings pypi_prod.url`; \
		VERSION=`python -c "print(__import__('devopsdriver').__version__)"`; \
		cd $(VENV_DIR)/test_published; \
		$(INITIAL_PYTHON) -m venv .venv; \
		$(SET_ENV); \
		pip install --no-cache-dir --log $@ -i $$TESTURL  $(LIBRARY)==$$VERSION --extra-index-url $$URL; \
		$(VENV_PYTHON) -m devopsdriver.settings pypi_test.repo
	@$(SET_ENV); \
		REPO=`$(VENV_PYTHON) -m devopsdriver.settings pypi_prod.repo`; \
		USERNAME=`$(VENV_PYTHON) -m devopsdriver.settings pypi_prod.username`; \
		PASSWORD=`$(VENV_PYTHON) -m devopsdriver.settings pypi_prod.password`; \
		$(VENV_PYTHON) -m twine upload --repository $$REPO dist/* --username $$USERNAME --password $$PASSWORD
	@echo Waiting for uploaded package to be avilable before testing
	@sleep $(SLEEP_TIME_IN_SECONDS)
	@$(SET_ENV); \
		URL=`$(VENV_PYTHON) -m devopsdriver.settings pypi_prod.url`; \
		VERSION=`python -c "print(__import__('devopsdriver').__version__)"`; \
		cd $(VENV_DIR)/test_published; \
		$(INITIAL_PYTHON) -m venv .venv; \
		$(SET_ENV); \
		pip install  --no-cache-dir --log $@ -i $$URL  $(LIBRARY)==$$VERSION; \
		$(VENV_PYTHON) -m devopsdriver.settings pypi_test.repo
	@touch $@

deploy: $(DEPLOY_FILE)



clean:
	@rm -Rf $(VENV_DIR)
	@rm -f $(strip $(COVERAGE_FILE))*
	@rm -Rf `find . -type d -name __pycache__`
	@rm -Rf .pytest_cache
	@rm -Rf dist
	@rm -Rf build
	@rm -Rf *.egg-info
	@find . -iname "*.pyc" -delete
