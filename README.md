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

### Apache Kafka KRaft variant

An alternative compose file (`compose-apache-kafka.yml`) runs the official Apache Kafka image in **KRaft mode** (without Zookeeper). Use the `-apache` Makefile targets:

```shell
make build-apache
make up-apache
make clean-apache
```

> **Troubleshooting:** If the Kafka container exits with an error like `Invalid cluster.id in /var/lib/kafka/data/meta.properties`, the persisted `kafka-data` volume contains a `cluster.id` from a previous run that no longer matches the current `CLUSTER_ID`. Run `make clean-apache` to remove the stale volume, then `make up-apache` again. To avoid this, pin a fixed `CLUSTER_ID` in `compose-apache-kafka.yml` under the `kafka` service's `environment` block.

#### Differences between the two compose files

| Aspect | `docker-compose.yml` (ZooKeeper) | `compose-apache-kafka.yml` (KRaft) |
|---|---|---|
| **Kafka image** | `confluentinc/cp-kafka:7.5.3` | `apache/kafka:latest` |
| **Coordination** | ZooKeeper (`confluentinc/cp-zookeeper:7.5.3`) | Self-managed via KRaft |
| **Services count** | 4: `api`, `worker`, `kafka`, `zookeeper` | 3: `api`, `worker`, `kafka` |
| **Required env vars** | `KAFKA_ZOOKEEPER_CONNECT`, broker id, listeners | `CLUSTER_ID`, `KAFKA_NODE_ID`, `KAFKA_PROCESS_ROLES`, `KAFKA_CONTROLLER_QUORUM_VOTERS`, listeners |
| **Volumes** | `kafka-data`, `kafka-secrets`, plus ZooKeeper data/log/secrets volumes | `kafka-data` only |
| **Use case** | Stable, production-like Confluent stack; legacy ZooKeeper deployments | Simpler, modern Apache Kafka stack; no external dependency on ZooKeeper |

#### KRaft vs. ZooKeeper mode

**ZooKeeper mode** (current `docker-compose.yml`)

Kafka traditionally relies on Apache ZooKeeper to store cluster metadata: broker membership, topic configuration, ACLs, and controller election. The Kafka broker connects to ZooKeeper at startup.

- **Pros:** battle-tested for many Kafka versions; required for older Kafka clusters.
- **Cons:** extra operational component to deploy, monitor, and secure; ZooKeeper can become a bottleneck and a source of complexity.

**KRaft mode** (new `compose-apache-kafka.yml`)

KRaft = Kafka Raft Metadata mode. Introduced in Kafka 2.8 and production-ready later, it removes ZooKeeper entirely. Kafka brokers themselves manage metadata using the Raft consensus protocol.

Key concepts in the new compose file:

- `CLUSTER_ID`: a fixed UUID that identifies the Kafka cluster. Must match the value stored in `meta.properties` in `kafka-data`.
- `KAFKA_NODE_ID: 1`: unique id for this broker/controller node.
- `KAFKA_PROCESS_ROLES: broker,controller`: this single node acts as both broker and controller.
- `KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:29093`: the Raft voters (here, just this one node on port `29093`).
- `KAFKA_LISTENERS`: two listeners — `PLAINTEXT://:29092` for clients and `CONTROLLER://:29093` for internal controller communication.
- `KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER`: tells Kafka which listener to use for the Raft quorum.

- **Pros:** simpler architecture, faster controller failover, easier deployment, no ZooKeeper dependency.
- **Cons:** requires newer Kafka versions; some legacy tooling still assumes ZooKeeper.

#### Official documentation

- Apache Kafka KRaft overview and configuration: https://kafka.apache.org/documentation/#kraft
- Apache Kafka Docker image quickstart: https://kafka.apache.org/documentation/#docker
- Confluent Platform Kafka with ZooKeeper: https://docs.confluent.io/platform/current/installation/docker/config-reference.html
- Kafka listeners explained: https://kafka.apache.org/documentation/#configuration_listeners

#### Manual `docker compose` commands

If you prefer to bypass `make`:

```shell
# ZooKeeper variant
docker compose -f docker-compose.yml build
docker compose -f docker-compose.yml up --remove-orphans
docker compose -f docker-compose.yml down -v --remove-orphans

# KRaft variant
docker compose -f compose-apache-kafka.yml build
docker compose -f compose-apache-kafka.yml up --remove-orphans
docker compose -f compose-apache-kafka.yml down -v --remove-orphans
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


