from editor.components.overlay.message_overlay import MessageOverlay
from editor.components.overlay import Overlay
import customtkinter as ctk
from editor.level.level import SAVE_FOLDER_PATH
from pathlib import Path


class LoadOverlay(Overlay):
    def __init__(self):
        super().__init__("load_file")

        self.geometry("300x250")

        label = ctk.CTkLabel(
            self,
            text="Choose a file to load.",
            corner_radius=10,
            width=280,
            height=100,
            wraplength=240,
        )
        label.pack(pady=2, side="top")

        interaction_container = ctk.CTkFrame(self, fg_color="transparent")
        interaction_container.pack(pady=4)

        self.files: dict[str, Path] = {}
        for file in [file for file in SAVE_FOLDER_PATH.iterdir() if file.is_file()]:
            self.files[file.name] = file

        self.option_menu = ctk.CTkOptionMenu(
            interaction_container, values=list(self.files.keys())
        )
        self.option_menu.grid(row=0, column=0, padx=4)

        load_button = ctk.CTkButton(
            interaction_container, text="Load", command=self._load, width=32
        )
        load_button.grid(row=0, column=1, padx=4)

    def _load(self):
        from editor.level import level_loader

        file_path = self.files[self.option_menu.get()]
        level_loader.load_level(file_path)

        self._close()

        MessageOverlay(
            "Sucessfully loaded the level.",
            button_commands={
                "Ok": lambda: None,
            },
        )
