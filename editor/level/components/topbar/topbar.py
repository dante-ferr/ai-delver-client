import customtkinter as ctk
from editor.level import level


class Topbar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        # self.pack_propagate(False)
        grid_toggle_var = ctk.BooleanVar(value=True)
        level.toggler.add_var(grid_toggle_var, "grid_lines")
        grid_toggle = ctk.CTkCheckBox(
            self,
            text="Grid",
            variable=grid_toggle_var,
            checkbox_width=20,
            checkbox_height=20,
        )
        grid_toggle.pack(pady=1, side="right")
