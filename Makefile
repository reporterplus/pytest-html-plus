.PHONY: build shell test lint clean

IMAGE_NAME = pytest-html-plus
SRC_DIR    = $(shell pwd)

# Mount local source into container — no rebuild needed on code changes
DOCKER_RUN = docker run --rm \
    -v $(SRC_DIR):/app \
    -w /app \
    $(IMAGE_NAME)

DOCKER_RUN_REPORTS = docker run --rm \
    -v $(SRC_DIR):/app \
    -w /app \
    $(IMAGE_NAME)

build:
	docker build -t $(IMAGE_NAME) .

build-with-dev-dependencies:
	docker build --build-arg INSTALL_DEV=true -t $(IMAGE_NAME) .

shell:
	docker run -it \
        -v $(SRC_DIR):/app \
        -w /app \
        $(IMAGE_NAME) /bin/bash

test:
	poetry run pytest tests/unit --reruns 1

test-with-xdist:
	$(DOCKER_RUN_REPORTS) poetry run poetry run pytest -s tests/unit --reruns 1 -n auto --upload 

lint:
	$(DOCKER_RUN) poetry run ruff check .

fix:
	$(DOCKER_RUN) poetry run ruff check . --fix
	$(DOCKER_RUN) poetry run ruff format .

install-formatter:
	$(DOCKER_RUN) sh -c "pip install pre-commit && pre-commit install"

clean:
	docker rmi $(IMAGE_NAME)
	rm -rf $(REPORTS_DIR)