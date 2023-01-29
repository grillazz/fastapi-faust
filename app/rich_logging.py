from rich.console import Console
from rich.logging import RichHandler


class RichConsoleHandler(RichHandler):
    """
    Rich console handler used to set a console width and style color.

    More information's:
        https://rich.readthedocs.io/en/stable/reference/logging.html#logging
    """

    def __init__(self, width=200, style=None, **kwargs):
        super().__init__(
            console=Console(color_system="256", width=width, style=style), **kwargs
        )
