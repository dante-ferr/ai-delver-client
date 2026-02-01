from app.components import IconButton
from tkinter import Menu
from src.config import config


class LoadButton(IconButton):

    def __init__(self, master, **kwargs):
        super().__init__(
            master, svg_path=str(config.ASSETS_PATH / "svg" / "load.svg"), **kwargs
        )
        self.option_menu: Menu | None = None
