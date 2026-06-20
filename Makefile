.PHONY: check test audit

check: test audit

test:
	python3 -m unittest discover -s Tests -p 'test_*.py'

audit:
	python3 scripts/config_security.py audit --root .
