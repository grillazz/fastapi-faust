import asyncio
import random
import time

import pytest
from punkreq.asyncio import Client


@pytest.mark.anyio
async def test_publish():
    async with Client(base_url="http://0.0.0.0:8080") as client:
        response = await client.post("/publish", json={"message": f"random: {random.random()!s}"})
        response.raise_for_status()


@pytest.mark.anyio
async def test_publish_sustained_maximum_speed_for_10_seconds():
    duration = 10.0
    async with Client(base_url="http://0.0.0.0:8080") as client:
        start = time.perf_counter()
        count = 0
        while time.perf_counter() - start < duration:
            response = await client.post(
                "/publish",
                json={"message": f"random: {random.random()!s}"},
            )
            response.raise_for_status()
            count += 1
        elapsed = time.perf_counter() - start
        print(f"Sustained load: {count} requests in {elapsed:.2f}s ({count / elapsed:.2f} req/s)")


@pytest.mark.anyio
async def test_publish_performance_4_workers_every_3_seconds():
    duration = 10.0
    interval = 3.0
    worker_count = 4
    iterations = int(duration // interval) + 1

    async with Client(base_url="http://0.0.0.0:8080") as client:
        start = time.perf_counter()

        async def worker(worker_id: int) -> int:
            count = 0
            for index in range(iterations):
                response = await client.post(
                    "/publish",
                    json={"message": f"worker-{worker_id}: {random.random()!s}"},
                )
                response.raise_for_status()
                count += 1
                if index + 1 < iterations:
                    await asyncio.sleep(interval)
            return count

        counts = await asyncio.gather(*(worker(worker_id) for worker_id in range(worker_count)))
        elapsed = time.perf_counter() - start
        total = sum(counts)
        print(f"4 workers every {interval:.0f}s: {total} req in {elapsed:.2f}s ({total / elapsed:.2f} req/s)")
