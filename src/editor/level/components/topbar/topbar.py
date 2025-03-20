import customtkinter as ctk
from editor.level import level
from .level_file_container import LevelFileContainer


class Topbar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        level_file_container = LevelFileContainer(self)
        level_file_container.pack(side="left", padx=2, pady=2)

        grid_toggle_var = ctk.BooleanVar(value=True)
        level.toggler.add_var(grid_toggle_var, "grid_lines")
        grid_toggle = ctk.CTkCheckBox(
            self,
            text="Grid",
            variable=grid_toggle_var,
            checkbox_width=20,
            checkbox_height=20,
        )
        grid_toggle.pack(pady=2, side="right")
