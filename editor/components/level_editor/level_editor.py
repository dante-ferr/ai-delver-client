import customtkinter as ctk
from .sidebar import Sidebar
from .level_canvas import LevelCanvas


class LevelEditor(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.selected_tool = "brush"

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        canvas = LevelCanvas(self)
        canvas.grid(row=0, column=0, sticky="nsew")

        sidebar = Sidebar(self)
        sidebar.grid(row=0, column=1, sticky="ns", padx=20, pady=20)

    def select_pen(self):
        self.selected_tool = "pen"
        print("Pen selected")

    def select_eraser(self):
        self.selected_tool = "eraser"
        print("Eraser selected")

    def save_level(self):
        print("Level saved")

    def load_level(self):
        print("Level loaded")
