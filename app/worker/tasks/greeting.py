import faust

from app.worker import get_faust_app


class Saluto(faust.Record):
    """A greeting message."""

    to_name: str = "World"
    from_name: str = "Faust"


faust_app = get_faust_app()
topic = faust_app.topic("saluti-argomento", value_type=Saluto)


@faust_app.agent(topic)
async def hello(greetings):
    async for greeting in greetings:
        print(f"Saluti veloci da {greeting.from_name} a {greeting.to_name}")
