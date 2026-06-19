.PHONY: build check lint test

SWIFTC ?= swiftc
ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

lint test build: check

check:
	@if command -v "$(SWIFTC)" >/dev/null 2>&1; then \
		SWIFTC="$(SWIFTC)" "$(ROOT)/scripts/run-projectile-math-tests.sh"; \
	else \
		echo "swiftc unavailable; executable projectile math tests skipped"; \
	fi
	python3 "$(ROOT)/scripts/check-baseline.py"
