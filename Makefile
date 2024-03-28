.PHONY: help clean check test report

.DEFAULT_GOAL := help

help: 	## Display this help message.
	@echo "Please use \`make <target>' where <target> is one of:"
	@awk -F ':.*?## ' '/^[a-zA-Z]/ && NF==2 {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

deps:  ## Rebuild dependency lock files
	pip-compile --strip-extras -o requirements.txt pyproject.toml
	pip-compile  --strip-extras --extra=dev -o requirements-dev.txt pyproject.toml

clean:  ## Format and lint clean
	ruff format src/
	ruff check --fix src/

check:  ## Lint check
	ruff check src/

test:  ## Test
	coverage run -m pytest
	coverage report

report:  ## Generate HTML coverage report
	coverage html
