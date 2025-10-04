from level_loader import level_loader
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .level_canvas import LevelCanvas


class CanvasScroller:
    def __init__(self, canvas: "LevelCanvas"):
        self.canvas = canvas
        self.canvas.after(1, self._center_canvas)

        self.last_x: int = 0
        self.last_y: int = 0

        self.scrolling = False

        self.min_zoom = 1
        self.max_zoom = 5

        self._bind_scroll_events()
        self.canvas.bind("<Configure>", self._on_resize)

    def _bind_scroll_events(self):
        self.canvas.bind("<ButtonPress-3>", self._start_scroll)
        self.canvas.bind("<B3-Motion>", self._on_scroll)
        self.canvas.bind("<ButtonRelease-3>", self._stop_scroll)
        # For Windows and MacOS
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        # For Linux
        self.canvas.bind("<Button-4>", self._on_mouse_wheel)
        self.canvas.bind("<Button-5>", self._on_mouse_wheel)

    def _on_resize(self, event):
        """Handle window resizing."""
        self.canvas.update_idletasks()
        self._center_canvas()

    def _start_scroll(self, event):
        """Start scrolling when the right mouse button is pressed."""
        self.scrolling = True
        self.scroll_start_x = event.x - self.last_x
        self.scroll_start_y = event.y - self.last_y

    def _on_scroll(self, event):
        """Scroll the canvas based on mouse movement."""
        if self.scrolling:
            scroll_x = int(event.x - self.scroll_start_x)
            scroll_y = int(event.y - self.scroll_start_y)
            scroll_x, scroll_y = self._clamp_scroll_position(scroll_x, scroll_y)

            self.canvas.scan_dragto(scroll_x, scroll_y, gain=1)
            self.last_x = scroll_x
            self.last_y = scroll_y

    def _clamp_scroll_position(self, x, y):
        """Clamp the scroll position to the canvas boundaries."""
        scale_x = self.canvas.zoom_level
        scale_y = self.canvas.zoom_level

        canvas_offset_x, canvas_offset_y = (
            self.canvas.draw_offset[0],
            self.canvas.draw_offset[1],
        )
        canvas_width, canvas_height = self.canvas_size
        level_width, level_height = (
            level_loader.level.map.size[0] * scale_x,
            level_loader.level.map.size[1] * scale_y,
        )

        min_x = -canvas_offset_x * scale_x - level_width + canvas_width // 2
        max_x = -canvas_offset_x * scale_x + canvas_width // 2

        min_y = -canvas_offset_y + -level_height + canvas_height // 2
        max_y = -canvas_offset_y + canvas_height // 2

        x = int(max(min_x, min(max_x, x)))
        y = int(max(min_y, min(max_y, y)))

        return x, y

    def _center_canvas(self):
        canvas_width, canvas_height = self.canvas_size
        level_width, level_height = level_loader.level.map.size
        canvas_center_x = canvas_width // 2 - level_width // 2
        canvas_center_y = canvas_height // 2 - level_height // 2

        self.canvas.scan_dragto(canvas_center_x, canvas_center_y, gain=1)
        self.last_x = canvas_center_x
        self.last_y = canvas_center_y

    def _on_mouse_wheel(self, event):
        """Handle mouse wheel scrolling for zooming."""
        current_zoom = self.canvas.zoom_level

        # Determine scroll direction
        if event.num == 5 or event.delta < 0:
            # Scroll down, zoom out
            new_zoom = max(self.min_zoom, current_zoom - 1)
        elif event.num == 4 or event.delta > 0:
            # Scroll up, zoom in
            new_zoom = min(self.max_zoom, current_zoom + 1)
        else:
            return

        if abs(new_zoom - current_zoom) > 1e-9:
            self.canvas.set_zoom_level(new_zoom, 0, 0)

    @property
    def canvas_size(self):
        return (self.canvas.winfo_width(), self.canvas.winfo_height())

    def _stop_scroll(self, event):
        """Stop scrolling when the right mouse button is released."""
        self.scrolling = False
