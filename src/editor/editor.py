from .level import level_loader
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
        self.minsize(width=800, height=600)

        self.level_editor: LevelEditor | None = None

        self.bind("<Button-1>", self.clear_focus)

        self.restart_level_editor()

    def restart_level_editor(self):
        if self.level_editor:
            self.level_editor.pack_forget()

        self.level_editor = LevelEditor(self)
        self.level_editor.pack(expand=True, fill="both")

    def clear_focus(self, event):
        widget_under_cursor = self.winfo_containing(event.x_root, event.y_root)

        parent_ctk_widget = self.get_parent_ctk_widget(widget_under_cursor)

        if parent_ctk_widget is None or not self.is_focusable(parent_ctk_widget):
            self.focus_set()

    def get_parent_ctk_widget(self, widget):
        """
        Traverse up the widget hierarchy to find the parent CTk widget.
        """
        while widget is not None:
            if isinstance(widget, (ctk.CTkBaseClass, ctk.CTk)):
                return widget
            widget = widget.master
        return None

    def is_focusable(self, widget):
        """
        Check if the widget is focusable (e.g., CTkEntry, CTkTextbox, CTkButton, etc.).
        """
        focusable_widgets = (
            ctk.CTkEntry,
            ctk.CTkTextbox,
            ctk.CTkButton,
        )
        return isinstance(widget, focusable_widgets)

    @property
    def level(self):
        return level_loader.level


app = App()
