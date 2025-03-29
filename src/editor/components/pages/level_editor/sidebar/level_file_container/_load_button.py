from editor.components import IconButton
from tkinter import Menu

from ._load_overlay import LoadOverlay


class LoadButton(IconButton):
    def __init__(self, parent):
        super().__init__(parent, svg_path="assets/svg/load.svg")
        self.option_menu: Menu | None = None

    def _on_click(self, event):
        load_overlay = LoadOverlay()
