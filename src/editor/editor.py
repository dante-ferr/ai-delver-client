from level_loader import level_loader
import customtkinter as ctk
from .components.pages.level_editor import LevelEditor
from .components.pages.runner import Runner
from .components import Navbar
from .theme import theme
import sys
from .components.pages import Page

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme(theme.path)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Custom Tkinter App")
        self.attributes("-zoomed", True)
        self.minsize(width=800, height=600)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.navbar = Navbar(self)
        self.navbar.grid(row=0, column=0, sticky="ew")

        self.page_container = ctk.CTkFrame(self, fg_color="transparent")
        self.page_container.grid(row=1, column=0, sticky="nsew")

        self.selected_page: Page | None = None
        self._create_pages()

        self.bind("<Button-1>", self.clear_focus)

    def restart_level_editor(self):
        if self.pages["level_editor"]:
            self.pages["level_editor"].pack_forget()

        self.pages["level_editor"] = LevelEditor(self)
        self.select_page("level_editor")

    def _create_pages(self):
        pages: dict[str, Page] = {
            "level_editor": LevelEditor(self),
            "runner": Runner(self),
        }
        self.pages = pages

        self.navbar.create_page_selectors(pages, default_page_name="level_editor")

    def select_page(self, page_name: str):
        page = self.pages[page_name]

        if self.selected_page is not None:
            self.selected_page.grid_forget()

        self.selected_page = page
        page.grid(row=1, column=0, sticky="nsew")

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


# if not hasattr(sys.modules[__name__], "_app_initialized"):
#     app = App()
#     setattr(sys.modules[__name__], "_app_initialized", True)
# else:
#     app = sys.modules[__name__].app
