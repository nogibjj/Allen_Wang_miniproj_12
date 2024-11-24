# Application-specific variables
APP_NAME = databricks-file-pipeline
DOCKER_USER = 31good
DOCKER_TAG = $(DOCKER_USER)/$(APP_NAME):latest

# Default make targets
all: install format lint test

# Install dependencies
install:
	pip install --upgrade pip && pip install -r requirements.txt

# Format Python files
format:
	black *.py mylib/*.py

# Lint codebase
lint:
	ruff check *.py mylib/*.py

# Run tests with coverage
test:
	python -m pytest --cov=main test_main.py

# Build Docker image
build:
	docker build -t $(DOCKER_TAG) .

# Run Docker container
run:
	docker run -p 5000:5000 $(DOCKER_TAG)

# Tag Docker image
tag:
	docker tag $(APP_NAME) $(DOCKER_TAG)

# Push Docker image to Docker Hub
push: tag
	docker push $(DOCKER_TAG)

# Clean up Docker resources
clean:
	docker rmi -f $(APP_NAME) $(DOCKER_TAG)
	docker rm -f $(APP_NAME)-container || true