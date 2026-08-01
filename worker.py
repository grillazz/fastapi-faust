import os

import faust

stream_app = faust.App(
    "demo-stream",
    broker=os.getenv("FAUST_BROKER_URL"),
)

events = stream_app.topic("events", value_type=str)

@stream_app.agent(events)
async def process(stream):
    async for event in stream:
        print(f"processed: {event}")

if __name__ == "__main__":
    stream_app.main()