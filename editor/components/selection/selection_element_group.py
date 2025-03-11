from typing import Callable, TYPE_CHECKING

Color = tuple[str, str] | str

if TYPE_CHECKING:
    import customtkinter as ctk
    from .selection_manager import SelectionManager


class SelectionElementGroup:
    def __init__(self, on_select: Callable, frame: "ctk.CTkFrame"):
        self.on_select = on_select
        self.frame = frame
        frame_children = frame.winfo_children()

        self.selected = False

        self._bind_events_on(frame)
        for child in frame_children:
            self._bind_events_on(child)

    def set_colors(self, active_color: Color, inactive_color: Color):
        self.active_color = active_color
        self.inactive_color = inactive_color

    def set_manager(self, manager):
        self.manager: SelectionManager = manager

    def _bind_events_on(self, element):
        element.bind("<Enter>", self._on_hover_enter)
        element.bind("<Leave>", self._on_hover_leave)
        element.bind("<Button-1>", self._on_click)

    def _on_hover_enter(self, event):
        if not self.selected:
            self.frame.configure(fg_color=self.active_color)

    def _on_hover_leave(self, event):
        if not self.selected:
            self.frame.configure(fg_color=self.inactive_color)

    def _on_click(self, event):
        self.manager.selected_element_group = self

    def select(self):
        self.selected = True
        self.frame.configure(fg_color=self.active_color)

    def deselect(self):
        self.selected = False
        self.frame.configure(fg_color=self.inactive_color)
