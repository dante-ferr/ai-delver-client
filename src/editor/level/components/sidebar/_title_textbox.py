import customtkinter as ctk
from editor.level import level_loader


class TitleTextbox(ctk.CTkTextbox):
    def __init__(self, parent):
        super().__init__(parent, height=4, wrap="none")

        self.insert("0.0", level_loader.level.name)
        self.bind("<KeyRelease>", self._update_name)

    def _update_name(self, event=None):
        level_loader.level.name = self.get("0.0", "end").strip()
