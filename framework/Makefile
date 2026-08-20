PY ?= venv/bin/python

.PHONY: all test scenarios truth-tables

all: test scenarios truth-tables

test:
	$(PY) -m unittest discover -s tests -v

scenarios:
	$(PY) run_scenarios.py --scenarios

truth-tables:
	$(PY) run_scenarios.py --truth-table
