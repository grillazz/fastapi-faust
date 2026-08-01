# fastapi-faust

[![Python Version](https://img.shields.io/badge/python-3.14%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141%2B-009688)](https://fastapi.tiangolo.com/)
[![Faust Streaming](https://img.shields.io/badge/Faust_Streaming-0.13.0-orange)](https://github.com/faust-streaming/faust)
[![uv](https://img.shields.io/badge/uv-managed-purple)](https://github.com/astral-sh/uv)

Example integration of [FastAPI](https://fastapi.tiangolo.com/) with [Faust - Python Stream Processing Fork](https://github.com/faust-streaming/faust) (`faust-streaming`).

This repository provides an opinionated backend example demonstrating how to run a FastAPI REST API alongside a Faust event streaming worker connected to Kafka.

---

## Project Overview

- **Version:** `0.1.0`
- **Python:** `>= 3.14`
- **Key Dependencies:**
  - `fastapi[all]` (>= 0.141.1)
  - `faust-streaming[ckafka,fast]` (0.13.0)
  - `ruff` (>= 0.16.1)
- **Infrastructure:** Kafka & Zookeeper (`docker-compose.yml`)

---

## Setup with `uv`

This project uses [`uv`](https://github.com/astral-sh/uv) for fast, reliable Python dependency and environment management.

### 1. Install `uv`

If you don't have `uv` installed, install it via the official installer:

```shell
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Dependencies

Sync dependencies and set up the local virtual environment:

```shell
uv sync
```

### 3. Running Locally with `uv`

Ensure Kafka and Zookeeper are running first (e.g., via `docker compose up kafka zookeeper`):

```shell
# Start Kafka and Zookeeper
docker compose up -d kafka zookeeper

# Run FastAPI application
export FAUST_BROKER_URL="kafka://localhost:29092"
uv run uvicorn app:app --host 0.0.0.0 --port 8080 --reload

# Run Faust Worker (in another terminal)
export FAUST_BROKER_URL="kafka://localhost:29092"
uv run python worker.py worker -l info
```

---

## Running with Docker Compose

You can spin up the full stack (API, Worker, Kafka, Zookeeper) with `docker compose` or `make`:

```shell
# Build images
make build

# Start services
make up

# Stop and reset containers and volumes
make clean
```

Or view available targets:

```shell
make help
```

---

## Usage Example

Once the API and worker services are running:

### Publish an Event

Send a `POST` request to the `/publish` endpoint:

```shell
curl -X 'POST' \
  'http://localhost:8080/publish' \
  -H 'Content-Type: application/json' \
  -d '{"message": "Hello Faust!"}'
```

### Response

```json
{
  "status": "queued",
  "message": "Hello Faust!"
}
```

### Worker Log Output

In your worker process or `fastapi-faust-worker-1` Docker container, you should see:

```text
processed: Hello Faust!
```

---

## Development

- **Formatting & Linting:**
  ```shell
  uv run ruff check .
  uv run ruff format .
  ```
- **Pre-commit Hooks:**
  ```shell
  uv run pre-commit install
  ```

