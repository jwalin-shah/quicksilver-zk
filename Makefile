PYTHON ?= python3

.PHONY: test quick-validate validate

test:
	$(PYTHON) -m pytest tests/ -q

quick-validate:
	$(PYTHON) -m pytest tests/ -q
	$(PYTHON) demos/quicksilver_demo.py
	$(PYTHON) demos/zk_einsum.py

validate: quick-validate
