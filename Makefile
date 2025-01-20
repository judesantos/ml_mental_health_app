
build:
	@python3 app/model_train_main.py

run:
	@python3 app/model_inference_main.py

deploy:
	@python3 app/app_main.py

check:
	@flake8 app/

clean:
	@rm -rf `find . -name __pycache__`
	@rm -rf .ruff_cache

runner: check run clean
builder: check build clean

all: check build run clean deploy

.DEFAULT_GOAL := all
.PHONY: build run check clean runner builder deploy all
