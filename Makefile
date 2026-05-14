PYTHON ?= python3

.PHONY: test quick-validate validate demo

test:
	$(PYTHON) -m pytest tests/ -q

demo:
	$(PYTHON) -m quicksilver demo all

quick-validate:
	$(PYTHON) -m quicksilver quick-validate

validate: quick-validate
