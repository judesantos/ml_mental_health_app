
build:
	@python3 app/ml/runner_builder.py

run:
	@python3 app/ml/runner_inference.py

check:
	@flake8 app/

clean:
	@rm -rf `find . -name __pycache__`
	@rm -rf .ruff_cache

runner: check run clean
builder: check build clean

all: check build run clean

.DEFAULT_GOAL := all
.PHONY: build run check clean runner builder