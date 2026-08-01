import asyncio
import os
from contextlib import asynccontextmanager

import faust
from fastapi import FastAPI
from pydantic import BaseModel

stream_app = faust.App(
    "demo-stream",
    broker=os.getenv("FAUST_BROKER_URL"),
)

events = stream_app.topic("events", value_type=str)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(stream_app.start())
    try:
        yield
    finally:
        await stream_app.stop()
        await task


app = FastAPI(lifespan=lifespan)


class Ingress(BaseModel):
    message: str


@app.post("/publish")
async def publish(payload: Ingress):
    await events.send(value=payload.message)
    return {"status": "queued", "message": payload.message}