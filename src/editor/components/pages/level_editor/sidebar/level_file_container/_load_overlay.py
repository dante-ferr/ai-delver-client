from editor.components.overlay.message_overlay import MessageOverlay
from editor.components.overlay import Overlay
import customtkinter as ctk
from level.level import SAVE_FOLDER_PATH
from pathlib import Path


class LoadOverlay(Overlay):
    def __init__(self):
        super().__init__("load_file")

        label = ctk.CTkLabel(
            self,
            text="Choose a file to load.",
            height=100,
            wraplength=240,
        )
        label.pack(pady=0, anchor="w", fill="x")

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

        self._post_init_config()

    def _load(self):
        from level import level_loader

        level_loader.load_level(self.files[self.option_menu.get()])
        self._restart_level_editor()

        self._close()

        MessageOverlay(
            "Sucessfully loaded the level.",
            button_commands={
                "Ok": lambda: None,
            },
        )

    def _restart_level_editor(self):
        from app_manager import app_manager

        app_manager.editor_app.restart_level_editor()
