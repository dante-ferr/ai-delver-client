from app.components import IconButton
from tkinter import Menu
from src.config import config


class LoadButton(IconButton):

    def __init__(self, master):
        super().__init__(master, svg_path=str(config.ASSETS_PATH / "svg" / "load.svg"))
        self.option_menu: Menu | None = None

    def _on_click(self, event):
        pass
