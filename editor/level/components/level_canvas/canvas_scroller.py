import customtkinter as ctk


class CanvasScroller:
    def __init__(self, canvas: ctk.CTkCanvas):
        self.canvas = canvas

        self.last_x: int = 0
        self.last_y: int = 0

        self.scrolling = False

        self._bind_scroll_events()

    def _bind_scroll_events(self):
        self.canvas.bind("<ButtonPress-3>", self._start_scroll)
        self.canvas.bind("<B3-Motion>", self._on_scroll)
        self.canvas.bind("<ButtonRelease-3>", self._stop_scroll)

    def _start_scroll(self, event):
        """Start scrolling when the right mouse button is pressed."""
        self.scrolling = True
        self.scroll_start_x = event.x - self.last_x
        self.scroll_start_y = event.y - self.last_y

    def _on_scroll(self, event):
        """Scroll the canvas based on mouse movement."""
        if self.scrolling:
            scroll_x = event.x - self.scroll_start_x
            scroll_y = event.y - self.scroll_start_y
            self.canvas.scan_dragto(scroll_x, scroll_y, gain=1)
            self.last_x = scroll_x
            self.last_y = scroll_y

    def _stop_scroll(self, event):
        """Stop scrolling when the right mouse button is released."""
        self.scrolling = False
