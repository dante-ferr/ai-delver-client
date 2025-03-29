import customtkinter as ctk
from .. import Page


class Runner(Page):
    def __init__(self, parent):
        super().__init__(parent, "Runner")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0, minsize=32)
        self.grid_rowconfigure(1, weight=1)

        upper_frame = ctk.CTkFrame(self, fg_color="transparent")
        upper_frame.grid(row=0, column=0, sticky="nsew")

        timeline_frame = ctk.CTkFrame(self, fg_color="white")
        timeline_frame.grid(row=1, column=0, sticky="nsew")
