# Default tests run with make test and make quick-tests
TESTS?=test
# Default environment for make tox
ENV?=py38
# Extra arguments supplied to tox command
ARGS?=
# Location of virtualenv used for development.
VENV?=.venv
# Source virtualenv to execute command (flake8, sphinx, twine, etc...)
IN_VENV=if [ -f $(VENV)/bin/activate ]; then . $(VENV)/bin/activate; fi;
# Use uv for commands if available, otherwise fall back to venv
UV_EXISTS := $(shell command -v uv 2>/dev/null)
ifneq ($(UV_EXISTS),)
RUN := uv run
else
RUN := $(IN_VENV)
endif
# TODO: add this upstream as a remote if it doesn't already exist.
UPSTREAM?=origin
SOURCE_DIR?=pydantictes
BUILD_SCRIPTS_DIR=scripts
DEV_RELEASE?=0
VERSION?=$(shell DEV_RELEASE=$(DEV_RELEASE) python3 $(BUILD_SCRIPTS_DIR)/print_version_for_release.py $(SOURCE_DIR) $(DEV_RELEASE))
PROJECT_URL?=https://github.com/jmchilton/pydantic-tes
PROJECT_NAME?=pydantic-tes
TEST_DIR?=tests

.PHONY: clean-pyc clean-build clean

help:
	@egrep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

setup-venv: ## setup a development virutalenv in current directory
	if command -v uv > /dev/null 2>&1; then \
		uv venv $(VENV) && uv pip install -e ".[testing]"; \
	else \
		if [ ! -d $(VENV) ]; then python3 -m venv $(VENV); fi; \
		$(IN_VENV) pip install -e ".[testing]"; \
	fi

setup-git-hook-lint: ## setup precommit hook for linting project
	cp $(BUILD_SCRIPTS_DIR)/pre-commit-lint .git/hooks/pre-commit

setup-git-hook-lint-and-test: ## setup precommit hook for linting and testing project
	cp $(BUILD_SCRIPTS_DIR)/pre-commit-lint-and-test .git/hooks/pre-commit

flake8: ## check style using flake8 for current Python (faster than lint)
	$(RUN) flake8 --max-complexity 11 $(SOURCE_DIR)  $(TEST_DIR)

lint: ## check style using tox and flake8 for Python 3.7 and Python 3.10
	$(RUN) tox -e py310-lint && tox -e py314-lint

lint-readme: dist ## check README formatting for PyPI
	$(RUN) twine check dist/*

test: ## run tests with the default Python (faster than tox)
	$(RUN) pytest $(TESTS)

tox: ## run tests with tox in the specified ENV
	$(RUN) tox -e $(ENV) -- $(ARGS)

open-project: ## open project on github
	open $(PROJECT_URL) || xdg-open $(PROJECT_URL)

dist: clean ## package
	$(RUN) python -m build
	$(RUN) twine check dist/*
	ls -l dist

commit-version: ## Update version and history, commit.
	$(RUN) DEV_RELEASE=$(DEV_RELEASE) python $(BUILD_SCRIPTS_DIR)/commit_version.py $(SOURCE_DIR) $(VERSION)

new-version: ## Mint a new version
	$(RUN) DEV_RELEASE=$(DEV_RELEASE) python $(BUILD_SCRIPTS_DIR)/new_version.py $(SOURCE_DIR) $(VERSION)

release-local: commit-version new-version

push-release: ## Push a tagged release to github
	git push $(UPSTREAM) main
	git push --tags $(UPSTREAM)

release: release-local push-release ## package, review, and upload a release

add-history: ## Reformat HISTORY.rst with data from Github's API
	$(RUN) python $(BUILD_SCRIPTS_DIR)/bootstrap_history.py $(ITEM)
