import customtkinter as ctk
from .level.components.level_editor import LevelEditor
from .theme import theme

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme(theme.path)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Custom Tkinter App")
        self.attributes("-zoomed", True)

        level_editor = LevelEditor(self)
        level_editor.pack(expand=True, fill="both")
