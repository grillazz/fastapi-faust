import random
import time

import pytest
from punkreq.asyncio import Client


@pytest.mark.anyio
async def test_publish():
    async with Client(base_url="http://0.0.0.0:8181") as client:
        response = await client.post("/publish", json={"message": f"random: {random.random()!s}"})
        response.raise_for_status()


@pytest.mark.anyio
async def test_publish_sustained_maximum_speed_for_10_seconds():
    duration = 10.0
    async with Client(base_url="http://0.0.0.0:8181") as client:
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
