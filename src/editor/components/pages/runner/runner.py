import customtkinter as ctk
from .. import Page
from .sidebar import Sidebar


class Runner(Page):
    def __init__(self, parent):
        super().__init__(parent, "Runner")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=128)
        self.grid_columnconfigure(1, weight=1)

        sidebar = Sidebar(self)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=16, pady=32)

        timeline_frame = ctk.CTkFrame(self, fg_color="black")
        timeline_frame.grid(row=0, column=1, sticky="nsew")
