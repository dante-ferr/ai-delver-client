import customtkinter as ctk
import platform


class MouseWheelScrollableFrame(ctk.CTkScrollableFrame):

    def __init__(self, master, *args, max_height: float | None = None, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.max_height = max_height

        self._bind_scroll_events()

    def _bind_scroll_events(self):
        system = platform.system()

        # For Windows/macOS (uses MouseWheel event with delta)
        if system in ["Windows", "Darwin"]:
            self.bind(
                "<Enter>",
                lambda _: self.bind_all("<MouseWheel>", self._on_mouse_scroll),
            )
            self.bind("<Leave>", lambda _: self.unbind_all("<MouseWheel>"))

        # For Linux (uses Button-4 and Button-5 for scroll)
        elif system == "Linux":
            self.bind(
                "<Enter>",
                lambda _: (
                    self.bind_all("<Button-4>", self._on_mouse_scroll),
                    self.bind_all("<Button-5>", self._on_mouse_scroll),
                ),
            )
            self.bind(
                "<Leave>",
                lambda _: (
                    self.unbind_all("<Button-4>"),
                    self.unbind_all("<Button-5>"),
                ),
            )

    def _on_mouse_scroll(self, event):
        system = platform.system()

        if system in ["Windows", "Darwin"]:  # Windows/macOS
            self._parent_canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

        elif system == "Linux":  # Linux (Ubuntu, etc.)
            if event.num == 4:  # Scroll up
                self._parent_canvas.yview_scroll(-1, "units")
            elif event.num == 5:  # Scroll down
                self._parent_canvas.yview_scroll(1, "units")

    def _update_scrollbar_visibility(self):
        """
        Dynamically show or hide the scrollbar based on content size.
        """
        content_height = sum(widget.winfo_height() for widget in self.winfo_children())
        frame_height = self.winfo_height()

        if content_height > frame_height:
            self._scrollbar.configure(width=16)
        else:
            self._scrollbar.configure(width=0)
