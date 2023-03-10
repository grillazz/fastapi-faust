import asyncio
import importlib
from typing import Optional

import faust
from fastapi import FastAPI

import app.worker as worker
from app.utils import get_logger

logger = get_logger(__name__)

app = FastAPI()


class Saluto(faust.Record):
    from_name: str
    to_name: str


@app.on_event("startup")
async def startup():
    logger.debug(f"asyncio.get_running_loop() = {asyncio.get_running_loop()}")
    # set up the faust app for the api
    worker.set_faust_app_for_api()

    app.state.faust = worker.get_faust_app()
    #
    app.state.faust.topic("saluti-argomento", value_type=Saluto)
    # start the faust app in client mode
    asyncio.create_task(app.state.faust.start_client())


@app.on_event("shutdown")
async def shutdown():
    app.state.faust = worker.get_faust_app()

    # graceful shutdown
    await app.state.faust.stop()


@app.post("/greeting")
async def get_increment(from_name: str | None = None, to_name: str | None = None):
    greeting_task = importlib.import_module(
        "app.worker.tasks.greeting",
    )
    await greeting_task.topic.send(
        value=Saluto(from_name, to_name),
    )

    return {"message": "Message sent. Ho Ho Ho!"}
