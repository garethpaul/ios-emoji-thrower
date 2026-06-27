.PHONY: build check lint test

SWIFTC ?= swiftc
override empty :=
override space := $(empty) $(empty)
override makefile_space := __IOS_EMOJI_THROWER_MAKEFILE_SPACE__
override encoded_makefile_list := $(patsubst $(makefile_space)%,%,$(subst $(space),$(makefile_space),$(MAKEFILE_LIST)))
override ROOT := $(subst $(makefile_space),$(space),$(abspath $(dir $(lastword $(encoded_makefile_list)))))

lint test build: check

check:
	@if command -v "$(SWIFTC)" >/dev/null 2>&1; then \
		SWIFTC="$(SWIFTC)" "$(ROOT)/scripts/run-projectile-math-tests.sh"; \
	else \
		echo "swiftc unavailable; executable projectile math tests skipped"; \
	fi
	python3 "$(ROOT)/scripts/check-baseline.py"
	python3 "$(ROOT)/scripts/test-make-spaced-path.py"
