import customtkinter as ctk
from ._draggable_box import DraggableBox


class SortableList(ctk.CTkScrollableFrame):
    """
    A list container that allows reordering its children via drag and drop
    using a placeholder to reserve space.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.boxes = []

        self.dragged_item = None
        self.drag_start_y_offset = 0
        self.placeholder_index = -1

        # Auto-scroll settings
        self.scroll_zone_height = 50  # Height of the activation zone (pixels)
        self.scroll_interval = (
            50  # Speed: Delay in ms between scrolls (higher = slower)
        )
        self.scroll_step = 2  # Amount to scroll per interval (units)
        self._is_scrolling = False
        self._scroll_direction = 0  # -1 (up), 0 (stop), 1 (down)

        self.placeholder = ctk.CTkFrame(
            self,
            fg_color="transparent",
            border_width=2,
            border_color=("gray60", "gray40"),
        )

        self._parent_canvas.bind("<Button-4>", self.on_mouse_wheel)
        self._parent_canvas.bind("<Button-5>", self.on_mouse_wheel)
        self._parent_canvas.bind("<MouseWheel>", self.on_mouse_wheel)

        self.bind("<Button-4>", self.on_mouse_wheel)
        self.bind("<Button-5>", self.on_mouse_wheel)
        self.bind("<MouseWheel>", self.on_mouse_wheel)

    def add_box(self, name, **kwargs):
        new_box = DraggableBox(self, name, **kwargs)
        self.boxes.append(new_box)
        new_box.pack(fill="x", pady=4, padx=(0, 8))

    def remove_box(self, name):
        for box in self.boxes:
            if box.name == name:
                box.destroy()
                self.boxes.remove(box)
                return
        print(f"Box '{name}' not found.")

    def get_order(self):
        return [box.name for box in self.boxes]

    def start_drag(self, item: DraggableBox, event):
        if self.dragged_item:
            return

        self.dragged_item = item
        self.placeholder_index = self.boxes.index(item)

        self.winfo_toplevel().bind("<ButtonRelease-1>", self.stop_drag, add="+")

        canvas = self._parent_canvas
        mouse_y_screen_relative = event.y_root - canvas.winfo_rooty()
        mouse_y_content = canvas.canvasy(mouse_y_screen_relative)
        self.drag_start_y_offset = mouse_y_content - item.winfo_y()

        self.placeholder.configure(height=item.winfo_height(), width=item.winfo_width())

        self._repack_layout(with_placeholder=True)
        item.lift()
        self._update_dragged_item_position(event)

    def perform_drag(self, event):
        if not self.dragged_item:
            return

        self._update_scroll_direction(event)
        self._update_dragged_item_position(event)
        self._calculate_placeholder_index(event)

    def stop_drag(self, event):
        self.winfo_toplevel().unbind("<ButtonRelease-1>")

        if not self.dragged_item:
            return

        self._is_scrolling = False
        self._scroll_direction = 0

        self.placeholder.pack_forget()
        self.dragged_item.place_forget()

        old_index = self.boxes.index(self.dragged_item)
        self.boxes.pop(old_index)

        target_index = self.placeholder_index
        if target_index > len(self.boxes):
            target_index = len(self.boxes)

        self.boxes.insert(target_index, self.dragged_item)

        self.dragged_item = None
        self.placeholder_index = -1

        self._repack_layout(with_placeholder=False)

    def on_mouse_wheel(self, event):
        if self.dragged_item:
            return

        if event.num == 5 or event.delta < 0:
            self._parent_canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self._parent_canvas.yview_scroll(-1, "units")

    def _update_scroll_direction(self, event):
        canvas = self._parent_canvas
        mouse_y_viewport = event.y_root - canvas.winfo_rooty()
        visible_height = canvas.winfo_height()

        if mouse_y_viewport < self.scroll_zone_height:
            self._scroll_direction = -1
        elif mouse_y_viewport > visible_height - self.scroll_zone_height:
            self._scroll_direction = 1
        else:
            self._scroll_direction = 0

        if self._scroll_direction != 0 and not self._is_scrolling:
            self._is_scrolling = True
            self._auto_scroll_loop(event)

    def _auto_scroll_loop(self, last_event):
        if not self.dragged_item or self._scroll_direction == 0:
            self._is_scrolling = False
            return

        self._parent_canvas.yview_scroll(
            self._scroll_direction * self.scroll_step, "units"
        )
        self._update_dragged_item_position(last_event)
        self._calculate_placeholder_index(last_event)

        self.after(self.scroll_interval, lambda: self._auto_scroll_loop(last_event))

    def _update_dragged_item_position(self, event):
        canvas = self._parent_canvas
        mouse_y_viewport = event.y_root - canvas.winfo_rooty()
        mouse_y_content = canvas.canvasy(mouse_y_viewport)
        final_y = mouse_y_content - self.drag_start_y_offset
        self.dragged_item.place(x=10, y=final_y, relwidth=0.9)

    def _calculate_placeholder_index(self, event):
        """Calculates where the placeholder should be."""
        mouse_y = event.y_root
        static_boxes = [b for b in self.boxes if b is not self.dragged_item]

        if not static_boxes:
            self._update_placeholder_if_changed(0)
            return

        # 1. FIX: Priority Override based on Auto-Scroll Intent
        # If we are actively scrolling, we force the index to the extremes.
        # This bypasses the "shaky" geometry checks during animation.
        if self._is_scrolling:
            if self._scroll_direction == 1:
                self._update_placeholder_if_changed(len(static_boxes))
                return
            elif self._scroll_direction == -1:
                self._update_placeholder_if_changed(0)
                return

        # 2. Viewport Boundary Checks (Mouse outside widget)
        viewport_top = self.winfo_rooty()
        viewport_bottom = viewport_top + self.winfo_height()

        if mouse_y < viewport_top:
            self._update_placeholder_if_changed(0)
            return
        elif mouse_y > viewport_bottom:
            self._update_placeholder_if_changed(len(static_boxes))
            return

        # 3. Standard Geometry Check (Mouse inside widget and not scrolling)
        new_index = len(static_boxes)
        for i, box in enumerate(static_boxes):
            center = box.winfo_rooty() + (box.winfo_height() / 2)
            if mouse_y < center:
                new_index = i
                break

        self._update_placeholder_if_changed(new_index)

    def _update_placeholder_if_changed(self, new_index):
        if new_index != self.placeholder_index:
            self.placeholder_index = new_index
            self._repack_layout(with_placeholder=True)

    def _repack_layout(self, with_placeholder: bool):
        for child in self.winfo_children():
            if child is not self.dragged_item:
                child.pack_forget()

        visual_boxes = [b for b in self.boxes if b is not self.dragged_item]

        if with_placeholder:
            idx = max(0, min(self.placeholder_index, len(visual_boxes)))
            visual_boxes.insert(idx, self.placeholder)

        for widget in visual_boxes:
            widget.pack(fill="x", padx=10, pady=5)
