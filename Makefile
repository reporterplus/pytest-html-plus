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

lint:
	docker run --rm pytest-html-plus poetry run ruff check .

fix:
	docker run --rm pytest-html-plus poetry run ruff check . --fix
	docker run --rm pytest-html-plus poetry run ruff format .

format:
	docker run --rm -v $(PWD):/app -w /app pytest-html-plus isort .
	docker run --rm -v $(PWD):/app -w /app pytest-html-plus black .

clean:
	docker rmi pytest-html-plus
