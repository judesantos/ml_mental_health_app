
# Check the code style using peop8 standard and flake8
check:
	@flake8 app/

# Build and train the model CLI
build:
	@python3 app/model_train_main.py

# Run the model inference CLI
run:
	@python3 app/model_inference_main.py

# Start the app frontend and backend
start:
	@python3 app/app_main.py

# Conda environment operations
install:
	@conda env create -f environment.yml

activate:
	@conda activate ml_ci_cd

# Cleanup project path
clean:
	@rm -rf `find . -name __pycache__`

.PHONY: install activate build run check clean start
#.DEFAULT_GOAL :=
