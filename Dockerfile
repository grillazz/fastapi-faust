FROM python:3.14.4-slim-trixie AS base

RUN apt-get update -qy \
    && apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    build-essential \
    ca-certificates

COPY --from=ghcr.io/astral-sh/uv:0.11.12 /uv /uvx /bin/

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON=python3.14.4 \
    UV_PROJECT_ENVIRONMENT=/faust

COPY pyproject.toml /_lock/
COPY uv.lock /_lock/

RUN cd /_lock && uv sync --locked --no-install-project
##########################################################################
FROM python:3.14.4-slim-trixie

ENV PATH=/faust/bin:$PATH

RUN groupadd -r faust
RUN useradd -r -d /faust -g faust -N faust

COPY --from=base --chown=faust:faust /faust /faust

USER faust
WORKDIR /faust
COPY app.py app/
COPY worker.py app/
COPY /tests/ tests/
COPY .env app/
COPY pyproject.toml /faust/pyproject.toml