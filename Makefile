.PHONY: build build-with-dev-dependencies shell test test-with-xdist lint fix install-formatter dist clean

IMAGE_NAME = pytest-html-plus
SRC_DIR    = $(shell pwd)

# Mount local source into container — no rebuild needed on code changes
DOCKER_RUN = docker run --rm \
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
	$(DOCKER_RUN) poetry run pytest tests/unit --reruns 1

test-with-xdist:
	$(DOCKER_RUN) poetry run pytest tests/unit --reruns 1 -n auto

lint:
	$(DOCKER_RUN) poetry run ruff check .

fix:
	$(DOCKER_RUN) poetry run ruff check . --fix
	$(DOCKER_RUN) poetry run ruff format .

install-formatter:
	poetry run pre-commit install

dist:
	poetry build

clean:
	docker rmi $(IMAGE_NAME)
