# Variables
APP_MODULE=main:app
HOST=0.0.0.0
PORT=8000
ENV_FILE=.env
PROJECT_DIR=$(shell pwd)

# Include the virtual environment activation script
SHELL := /bin/bash
VENV_ACTIVATE := . ./activate_venv.sh

# Open the default browser to the specified URL
browse:
	$(if $(shell which xdg-open), xdg-open http://127.0.0.1:8000/graphql, \
	$(if $(shell which open), open http://127.0.0.1:8000/graphql, \
	$(error No suitable command found to open the browser)))
	
# Entry to run the FastAPI application
run:
	$(VENV_ACTIVATE) && (cd $(PROJECT_DIR)/lawyers && uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT) --reload --env-file $(ENV_FILE))

# Entry to run tests
tests:
	$(VENV_ACTIVATE) && (cd $(PROJECT_DIR) && pytest tests/*)

# Clean up __pycache__ and other Python-generated files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

# Entry to install dependencies
install:
	$(VENV_ACTIVATE) && (cd $(PROJECT_DIR) && pip install -r requirements.txt)

# Entry to install dev-dependencies
dev:
	(cd $(PROJECT_DIR) && pip install -r requirements-dev.txt)


.PHONY: run tests clean install dev browse


