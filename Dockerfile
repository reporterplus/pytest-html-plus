FROM mcr.microsoft.com/playwright/python:v1.46.0-jammy
ENV POETRY_HOME="/opt/poetry" \
    PATH="/opt/poetry/bin:$PATH" \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --with dev

COPY . .
RUN poetry install --with dev

