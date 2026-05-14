PYTHON ?= python3

.PHONY: test quick-validate validate demo

test:
	$(PYTHON) -m pytest tests/ -q

demo:
	$(PYTHON) -m quicksilver demo all

quick-validate:
	$(PYTHON) -m pytest tests/ -q
	$(PYTHON) -m quicksilver demo quicksilver_demo.py
	$(PYTHON) -m quicksilver demo zk_einsum.py

validate: quick-validate
