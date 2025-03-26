import customtkinter as ctk
from ._save_button import SaveButton
from ._load_button import LoadButton


class LevelFileContainer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        save_button = SaveButton(self)
        save_button.pack(side="left", padx=3.2, pady=0)

        load_button = LoadButton(self)
        load_button.pack(padx=2, pady=0)
