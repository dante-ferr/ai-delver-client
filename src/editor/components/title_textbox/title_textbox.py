import customtkinter as ctk
from level_loader import level_loader


class TitleTextbox(ctk.CTkTextbox):
    def __init__(self, parent, default_text=""):
        super().__init__(parent, height=4, wrap="none")

        self.insert("0.0", default_text)
        self.bind("<KeyRelease>", self._update_name)

    def _get_input(self):
        """Get the current text from the textbox. Must be called in the _update_name method."""
        return self.get("0.0", "end").strip()

    def _update_name(self, event=None):
        """Update the level name based on the textbox content. Must be overridden in subclasses."""
        pass
