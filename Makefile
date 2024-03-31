.PHONY:clean venv test coverage lint format
all:clean test coverage lint

MIN_TEST_COVERAGE=100
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
REQUIREMENTS=requirements.txt
INFRASTRUCTURE=requirements-infrastructure.txt

$(VENV_DIR)/touchfile: $(REQUIREMENTS)
	@test -d $(VENV_DIR) || $(INITIAL_PYTHON) -m venv $(VENV_DIR)
	@echo Ensuring pip is latest version
	@$(SET_ENV); $(VENV_PIP) install --quiet --upgrade pip
	@echo Fetching requirements
	@$(SET_ENV); $(VENV_PIP) install --quiet --upgrade --requirement $^
	@touch $@

venv: $(VENV_DIR)/touchfile

$(COVERAGE_FILE): $(VENV_DIR)/touchfile $(SOURCES) $(TESTS)
	@$(SET_ENV); $(VENV_PIP) install -q -r $(INFRASTRUCTURE)
	@$(SET_ENV); $(VENV_PYTHON) -m coverage run  --source $(LIBRARY) -m pytest

test: $(COVERAGE_FILE)

coverage: $(COVERAGE_FILE)
	@$(SET_ENV); $(VENV_PYTHON) -m coverage report -m --sort=cover --skip-covered --fail-under=$(MIN_TEST_COVERAGE)
	@if grep -q "test+coverage&message=$(MIN_TEST_COVERAGE)%" README.md; then true; else echo "Update README.md test coverage" && false; fi
	

$(FORMAT_FILE): $(VENV_DIR)/touchfile $(SOURCES)
	@$(SET_ENV); $(VENV_PIP) install -q -r $(INFRASTRUCTURE)
	@$(SET_ENV); $(VENV_PYTHON) -m black $(LIBRARY) &> $@

format: $(FORMAT_FILE)
	@cat $^

$(LINT_FILE): $(VENV_DIR)/touchfile $(SOURCES)
	@$(SET_ENV); $(VENV_PIP) install -q -r $(INFRASTRUCTURE)
	-@$(SET_ENV); $(VENV_PYTHON) -m pylint $(LIBRARY) &> $@
	-@$(SET_ENV); $(VENV_PYTHON) -m black $(LIBRARY) --check >> $@  2>&1

lint: $(LINT_FILE)
	@cat $^

clean:
	@rm -Rf $(VENV_DIR)
	@rm -f $(strip $(COVERAGE_FILE))*
	@rm -Rf .pytest_cache
	@find . -iname "*.pyc" -delete
