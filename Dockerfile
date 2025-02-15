FROM python:3.13.1-alpine

LABEL authors="defuzia"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /app

RUN apk update && \
    apk add --no-cache python3-dev \
    gcc \
    musl-dev \
    libpq-dev \
    nmap

ADD pyproject.toml /app

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . /app/
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh