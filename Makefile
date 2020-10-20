.DEFAULT_GOAL := help
SHELL         := /bin/bash

# version control
export VCS_URL    := $(shell git config --get remote.origin.url)
export VCS_REF    := $(shell git rev-parse --short HEAD)
export BUILD_DATE := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")

OUTDIR := out


.PHONY: help
help: ## help on rule's targets
	@awk --posix 'BEGIN {FS = ":.*?## "} /^[[:alpha:][:space:]_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


.venv:
	# installing virtualenv
	python3 -m venv .venv
	# upgrading packages
	.venv/bin/pip install -U \
		pip \
		setuptools \
		wheel
	# installing basic tooling
	.venv/bin/pip install \
		pip-tools \
		pre-commit
	# Installing pre-commit hooks in current .git repo
	@.venv/bin/pre-commit install


.vscode/settings.json: .vscode/settings.template.json
	cp $< $@

.PHONY: testsenv devenv
devenv testsenv: .venv .vscode/settings.json ## test or develoment environments
	.venv/bin/pip install -r tools/requirements/$(subst env,,$@).txt


.PHONY: tests tests-dev
tests tests-dev: ## tests w/o or w/ dev options
	pytest $(if $(subst tests,,$@),--failed-first --pdb,)  \
		-vv \
		--durations=10 \
		--junitxml=${OUTDIR}/pytest-junit.xml \
		tools/tests


.PHONY: bundle
bundle: ## creates data bundle artifacts
	python3 tools/cli.py ${OUTDIR}


#.PHONY: schemas
#schemas: ## auto-generates *.meta.json files
#	python3 tools/cli.py



.PHONY: autoformat
autoformat: ## runs black python formatter on this service's code. Use AFTER make install-*
	# sort imports
	@python3 -m isort --atomic -rc $(CURDIR)
	# auto formatting with black
	@python3 -m black --verbose \
		--exclude "/(\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|\.svn|_build|buck-out|build|dist|migration|client-sdk|generated_code)/" \
		$(CURDIR)


.PHONY: clean
_GIT_CLEAN_ARGS = -dxf -e .vscode
clean: ## cleans all unversioned files in project and temp files create by this makefile
	# Cleaning unversioned
	@git clean -n $(_GIT_CLEAN_ARGS)
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	@echo -n "$(shell whoami), are you REALLY sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	@git clean $(_GIT_CLEAN_ARGS)