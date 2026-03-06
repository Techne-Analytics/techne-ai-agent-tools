PYTHON ?= python3
ifneq ("$(wildcard .venv/bin/python)","")
PYTHON := .venv/bin/python
endif

.PHONY: validate-plugins test test-skills-spec

validate-plugins:
	$(PYTHON) scripts/validate_plugins.py

test:
	$(PYTHON) -m pytest tests -v

test-skills-spec:
	$(PYTHON) -m pytest tests/skills/test_*_spec.py -v
