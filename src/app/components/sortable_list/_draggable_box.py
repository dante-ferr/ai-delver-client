import customtkinter as ctk
from src.config import config
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from sortable_list import SortableList


class DraggableBox(ctk.CTkFrame):
    """
    A subcomponent representing a single ordered box.
    """

    def __init__(self, master: "SortableList", name: str, **kwargs):
        super().__init__(master, **kwargs)
        self.name = name

        self.configure(
            fg_color=("gray80", "gray20"),
            corner_radius=6,
            border_width=1,
            border_color="gray50",
        )

        self.label = ctk.CTkLabel(
            self,
            text=name,
            font=ctk.CTkFont(size=config.STYLE.FONT.STANDARD_SIZE),
            anchor="w",
            padx=10,
        )
        self.label.pack(fill="both", expand=True)

        self.bind("<Button-1>", self._on_press)
        self.bind("<B1-Motion>", self._on_drag)
        # Note: We rely on the parent's global release bind for stopping drag securely now,
        # but we keep this for local consistency.
        self.bind("<ButtonRelease-1>", self._on_release)

        self.label.bind("<Button-1>", self._on_press)
        self.label.bind("<B1-Motion>", self._on_drag)
        self.label.bind("<ButtonRelease-1>", self._on_release)

        self.bind("<Button-4>", self._on_scroll)
        self.bind("<Button-5>", self._on_scroll)
        self.bind("<MouseWheel>", self._on_scroll)

        self.label.bind("<Button-4>", self._on_scroll)
        self.label.bind("<Button-5>", self._on_scroll)
        self.label.bind("<MouseWheel>", self._on_scroll)

    def _on_press(self, event):
        self.typed_master.start_drag(self, event)

    def _on_drag(self, event):
        self.typed_master.perform_drag(event)

    def _on_release(self, event):
        # We still call this, but the heavy lifting is done by the global bind in the list
        self.typed_master.stop_drag(event)

    def _on_scroll(self, event):
        self.typed_master.on_mouse_wheel(event)

    @property
    def typed_master(self) -> "SortableList":
        return cast("SortableList", self.master)
