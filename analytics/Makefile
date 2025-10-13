# Delete target on error.
# https://www.gnu.org/software/make/manual/html_node/Errors.html#Errors
# > This is almost always what you want make to do, but it is not historical
# > practice; so for compatibility, you must explicitly request it
.DELETE_ON_ERROR:

# Global tasks.
# =============================================================================
REQUIREMENTS_PATH ?= requirements.txt

VIRTUAL_ENV ?= .venv
export PATH := $(VIRTUAL_ENV)/bin:$(PATH)

.PHONY: venv

$(VIRTUAL_ENV): $(REQUIREMENTS_PATH)
	uv venv
	uv pip install -r $^
	touch $@

venv: $(VIRTUAL_ENV)

# Quality
# =============================================================================
.PHONY: fix quality

LINTER_CHECKED_DIRS := analyses macros metabase_scanner models seeds snapshots tests
SQLFLUFF_OPTIONS := --disable-progress-bar

fix: $(VIRTUAL_ENV)
	ruff format $(LINTER_CHECKED_DIRS)
	ruff check --fix $(LINTER_CHECKED_DIRS)
	sqlfluff fix $(SQLFLUFF_OPTIONS) $(LINTER_CHECKED_DIRS)

quality: $(VIRTUAL_ENV)
	ruff format --check $(LINTER_CHECKED_DIRS)
	ruff check $(LINTER_CHECKED_DIRS)
	sqlfluff lint $(SQLFLUFF_OPTIONS) $(LINTER_CHECKED_DIRS)
