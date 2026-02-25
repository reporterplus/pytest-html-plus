.PHONY: build shell test lint clean

build:
	docker build -t pytest-html-plus .

build-with-dev-dependencies:
	docker build --build-arg INSTALL_DEV=true -t pytest-html-plus .

shell:
	docker run -it pytest-html-plus /bin/bash

test:
	docker run --rm pytest-html-plus poetry run pytest tests/unit --reruns 1

test-with-xdist:
	docker run --rm pytest-html-plus poetry run pytest tests/unit --reruns 1 -n auto

install-formatter:
	pip install pre-commit
	pre-commit install

lint:
	docker run --rm pytest-html-plus poetry run ruff check .

fix:
	docker run --rm pytest-html-plus poetry run ruff check . --fix
	docker run --rm pytest-html-plus poetry run ruff format .


clean:
	docker rmi pytest-html-plus
