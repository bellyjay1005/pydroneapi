export DOCKER_BUILDKIT=1

AWS_DEFAULT_REGION?=us-east-2
IMAGE_NAME=pydroneapi
PROJECT=$(IMAGE_NAME)
VERSION?=latest
ANCHORE_ENGINE_URL?=https://ci-tools.anchore.io/inline_scan-latest

.DEFAULT_GOAL:=help

.PHONY: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

# BUILD
build-%: ## Global command to build local development image
	docker build \
		--ssh default \
		-t $(IMAGE_NAME):$* \
		--target $* .

build: ## Build local testing image
	make build-test

# DEVELOP
develop: build-test ## Launch a local development environment
	docker run -it --rm \
		-v ${PWD}:/work \
		-w /work \
		-e AWS_DEFAULT_REGION=$(AWS_DEFAULT_REGION) \
		$(IMAGE_NAME):test ash

# TEST
lint: ## Lint python code base
	python -m pylint $(PROJECT)

security-lint: ## Static analysis on common python vulnerabilities
	bandit -r $(PROJECT) -x setup.py

cve-check: ## Check dependencies for known CVEs
	safety check --full-report

pytest-%: ## Global pytest commands
	python -m pytest -vv \
		-W ignore::DeprecationWarning \
		--cov-report term-missing \
		--cov=$(PROJECT) \
		--cov-fail-under=$(COV) \
		tests/$*

unit: ## Run unit test on package methods
	make pytest-unit COV=90

e2e: ## Run end-to-end test on package methods
	make pytest-e2e COV=80

test-%: build-test ## Global testing commands
	docker run -it --rm \
		-v ${PWD}:/work \
		-w /work \
		-e AWS_DEFAULT_REGION=$(AWS_DEFAULT_REGION) \
		$(IMAGE_NAME):test \
		make $*

test: ## Run all testing commands. Designed to be implemented with a CI.
ifeq ($(CI),)
	$(eval CMD=test-)
else
	$(eval CMD:=)
endif
	make $(CMD)lint
	make $(CMD)security
	make $(CMD)unit
#	make $(CMD)e2e

.PHONY: develop test
