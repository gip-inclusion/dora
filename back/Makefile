# Delete target on error.
# https://www.gnu.org/software/make/manual/html_node/Errors.html#Errors
# > This is almost always what you want make to do, but it is not historical
# > practice; so for compatibility, you must explicitly request it
.DELETE_ON_ERROR:

# Global tasks.
# =============================================================================
REQUIREMENTS_PATH ?= requirements/dev.txt

VIRTUAL_ENV ?= .venv
export PATH := $(VIRTUAL_ENV)/bin:$(PATH)

.PHONY: compile-deps venv

$(VIRTUAL_ENV): $(REQUIREMENTS_PATH)
	uv venv
	uv pip install --require-hashes -r $^
	touch $@

venv: $(VIRTUAL_ENV)

PIP_COMPILE_FLAGS := --no-strip-extras --generate-hashes $(PIP_COMPILE_OPTIONS)
compile-deps:
	uv pip compile $(PIP_COMPILE_FLAGS) --output-file requirements/base.txt requirements/base.in
	uv pip compile $(PIP_COMPILE_FLAGS) --output-file requirements/test.txt requirements/test.in
	uv pip compile $(PIP_COMPILE_FLAGS) --output-file requirements/dev.txt requirements/dev.in
	uv pip compile $(PIP_COMPILE_FLAGS) --output-file requirements/prod.txt requirements/prod.in

# Quality
# =============================================================================
.PHONY: fix quality

LINTER_CHECKED_DIRS := config dora scripts

fix: $(VIRTUAL_ENV)
	ruff format $(LINTER_CHECKED_DIRS)
	ruff check --fix $(LINTER_CHECKED_DIRS)
	djhtml --tabwidth=2 $(LINTER_CHECKED_DIRS)

quality: $(VIRTUAL_ENV)
	# Vérification de la compilation des sources Python
	python -m compileall -q .
	# Linting et formatage du code Python
	ruff format --check $(LINTER_CHECKED_DIRS)
	ruff check $(LINTER_CHECKED_DIRS)
	# Vérification Django
	python manage.py check
	python manage.py makemigrations --check --dry-run --noinput
	# Vérification des fichier HTML et templates
	djhtml --tabwidth=2 --check $(LINTER_CHECKED_DIRS)

# Django.
# =============================================================================
.PHONY: populate_db runserver

populate_db: $(VIRTUAL_ENV)
	python manage.py import_admin_express
	python manage.py loaddata dora/structures/fixtures/01_structure_national_labels.json.gz

runserver: $(VIRTUAL_ENV)
	python manage.py runserver $(RUNSERVER_DOMAIN)

# Tests.
# =============================================================================

.PHONY: test

test: $(VIRTUAL_ENV)
	pytest
