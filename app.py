import os

from fastapi import FastAPI
from pydantic import BaseModel
import faust

app = FastAPI()

stream_app = faust.App(
    "demo-stream",
    broker=os.getenv("FAUST_BROKER_URL"),
)

events = stream_app.topic("events", value_type=str)

class Ingress(BaseModel):
    message: str

@app.post("/publish")
async def publish(payload: Ingress):
    await events.send(value=payload.message)
    return {"status": "queued", "message": payload.message}