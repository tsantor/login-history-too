# -----------------------------------------------------------------------------
# Generate help output when running just `make`
# -----------------------------------------------------------------------------
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

# -----------------------------------------------------------------------------

python_version=3.13.1

# START - Generic commands
# -----------------------------------------------------------------------------
# Environment
# -----------------------------------------------------------------------------

env:  ## Create virtual environment
	uv venv --python ${python_version}

env_remove:  ## Remove virtual environment
	rm -rf .venv

sqllite_remove:	## Remove sqlite database
	rm -f db.sqlite3

env_recreate: sqllite_remove env_remove env pip_install migrations migrate superuser serve ## Recreate environment from scratch

# -----------------------------------------------------------------------------
# Pip
# -----------------------------------------------------------------------------

pip_install:  ## Install requirements
	uv pip install --upgrade pip
	@for file in $$(ls requirements/*.txt); do \
			uv pip install -r $$file; \
	done
	pre-commit install

pip_install_editable:  ## Install in editable mode
	uv pip install -e .

pip_list:  ## Run pip list
	uv pip list

pip_freeze:  ## Run pipfreezer freeze
	pipfreezer freeze  --verbose

pip_upgrade:  ## Run pipfreezer upgrade
	pipfreezer upgrade  --verbose

# -----------------------------------------------------------------------------
# Django
# -----------------------------------------------------------------------------

manage:	## Run django manage.py (eg - make manage cmd="shell")
	python3 manage.py ${cmd}

superuser:  ## Create superuser
	python3 manage.py createsuperuser

migrations:  ## Create migrations (eg - make migrations app="core")
	python3 manage.py makemigrations ${app}

migrate:  ## Apply migrations
	python3 manage.py migrate

serve:  ## Run server
	python3 manage.py runserver 127.0.0.1:8000

show_urls:  ## Show urls
	python3 manage.py show_urls

shell:  ## Run shell
	python3 manage.py shell_plus

flush:  ## Flush database
	python3 manage.py flush

# -----------------------------------------------------------------------------
# Testing
# -----------------------------------------------------------------------------

pytest:  ## Run tests
	pytest -vx

pytest_verbose:  ## Run tests in verbose mode
	pytest -vs

coverage:  ## Run tests with coverage
	coverage run -m pytest && coverage html

coverage_verbose:  ## Run tests with coverage in verbose mode
	coverage run -m pytest -vs && coverage html

coverage_skip:  ## Run tests with coverage and skip covered
	coverage run -m pytest -vs && coverage html --skip-covered

open_coverage:  ## Open coverage report
	open htmlcov/index.html

# -----------------------------------------------------------------------------
# Ruff
# -----------------------------------------------------------------------------

ruff_format: ## Run ruff format
	ruff format src/login_history_too

ruff_check: ## Run ruff check
	ruff check src/login_history_too

ruff_clean: ## Run ruff clean
	ruff clean

# -----------------------------------------------------------------------------
# Cleanup
# -----------------------------------------------------------------------------

clean_build: ## Remove build artifacts
	rm -fr build/ dist/ .eggs/
	find . -name '*.egg-info' -o -name '*.egg' -exec rm -fr {} +

clean_pyc: ## Remove python file artifacts
	find . \( -name '*.pyc' -o -name '*.pyo' -o -name '*~' -o -name '__pycache__' \) -exec rm -fr {} +

clean: clean_build clean_pyc ## Remove all build and python artifacts

clean_pytest_cache:  ## Clear pytest cache
	rm -rf .pytest_cache

clean_ruff_cache:  ## Clear ruff cache
	rm -rf .ruff_cache

clean_tox_cache:  ## Clear tox cache
	rm -rf .tox

clean_coverage:  ## Clear coverage cache
	rm .coverage
	rm -rf htmlcov

clean_tests: clean_pytest_cache clean_ruff_cache clean_tox_cache clean_coverage  ## Clear pytest, ruff, tox, and coverage caches

# -----------------------------------------------------------------------------
# Miscellaneous
# -----------------------------------------------------------------------------

tree:  ## Show directory tree
	tree -I 'build|dist|htmlcov|node_modules|migrations|contrib|__pycache__|*.egg-info|staticfiles|media'

# -----------------------------------------------------------------------------
# Deploy
# -----------------------------------------------------------------------------

dist: clean ## Builds source and wheel package
	uv build

twine_upload_test: dist ## Upload package to pypi test
	twine upload dist/* -r pypitest

twine_upload: dist ## Package and upload a release
	twine upload dist/*

twine_check: dist ## Twine check
	twine check dist/*

# END - Generic commands
# -----------------------------------------------------------------------------
# Project Specific
# -----------------------------------------------------------------------------

# Add project specific targets here
