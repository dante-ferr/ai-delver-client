import customtkinter as ctk
from .level.components.level_editor import LevelEditor
from .theme import theme
from .level import level

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme(theme.path)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Custom Tkinter App")
        self.attributes("-zoomed", True)
        self.minsize(width=800, height=600)

        level_editor = LevelEditor(self)
        level_editor.pack(expand=True, fill="both")
