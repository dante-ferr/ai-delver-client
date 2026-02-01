import customtkinter as ctk
from src.config import config
from ._delete_button import DeleteButton
from typing import TYPE_CHECKING, cast, Callable, Sequence

if TYPE_CHECKING:
    from sortable_list import SortableList


class DraggableBox(ctk.CTkFrame):
    """
    A subcomponent representing a single ordered box.
    """

    def __init__(
        self, master: "SortableList", name: str, remove_box_button=False, **kwargs
    ):
        super().__init__(master, **kwargs)
        self.name = name
        self.remove_box_button = remove_box_button

        self.default_color = ("gray80", "gray20")
        self.hover_color = ("gray75", "gray25")

        self._setup_ui()
        self._setup_bindings()

    def _setup_ui(self):
        self.configure(
            fg_color=self.default_color,
            corner_radius=6,
            border_width=1,
            border_color="gray50",
        )

        self.label = ctk.CTkLabel(
            self,
            text=self.name,
            font=ctk.CTkFont(size=config.STYLE.FONT.STANDARD_SIZE),
            anchor="w",
            padx=10,
        )
        self.label.pack(fill="both", expand=True)

        if self.remove_box_button:
            self.delete_button = DeleteButton(self, command=self._on_delete)
            # Initially hidden, placed on hover

    def _setup_bindings(self):
        """Consolidates local event bindings."""
        main_targets = [self, self.label]

        self._bind_events(
            main_targets,
            {
                "<Button-1>": self._on_press,
                "<B1-Motion>": self._on_drag,
                "<ButtonRelease-1>": self._on_release,
            },
        )

        self._bind_events(
            main_targets, {"<Enter>": self._on_enter, "<Leave>": self._on_leave}
        )

        # Note: Scroll logic is handled by the parent SortableList/MouseWheelScrollableFrame

    def _bind_events(
        self, widgets: Sequence[ctk.CTkBaseClass], events: dict[str, Callable]
    ):
        for widget in widgets:
            for sequence, handler in events.items():
                widget.bind(sequence, handler)

    def _on_delete(self):
        self.typed_master.remove_box(self.name)

    def _on_enter(self, event):
        self.configure(fg_color=self.hover_color)

        if self.remove_box_button:
            if not self.delete_button.winfo_viewable():
                self.delete_button.place(relx=1.0, x=-4, y=4, anchor="ne")
                self.delete_button.lift()
                self._monitor_mouse()

    def _on_leave(self, event):
        self.after(50, self._check_hover_state)

    def _monitor_mouse(self):
        """
        Periodically checks if mouse is inside the widget.
        Handles cases where scroll moves the widget away from the mouse.
        """
        if not self.winfo_exists() or not self.delete_button.winfo_viewable():
            return

        self._check_hover_state()

        if self.delete_button.winfo_viewable():
            self.after(200, self._monitor_mouse)

    def _check_hover_state(self):
        """Hides the delete button if the mouse is outside the frame bounds."""
        if not self.winfo_exists():
            return

        x, y = self.winfo_pointerxy()
        widget_x = self.winfo_rootx()
        widget_y = self.winfo_rooty()
        w = self.winfo_width()
        h = self.winfo_height()

        is_inside = (widget_x <= x <= widget_x + w) and (widget_y <= y <= widget_y + h)

        if not is_inside:
            self.configure(fg_color=self.default_color)
            if self.remove_box_button:
                self.delete_button.place_forget()

    def _on_press(self, event):
        self.typed_master.start_drag(self, event)

    def _on_drag(self, event):
        self.typed_master.perform_drag(event)

    def _on_release(self, event):
        self.typed_master.stop_drag(event)

    @property
    def typed_master(self) -> "SortableList":
        return cast("SortableList", self.master)
