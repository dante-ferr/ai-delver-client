from editor.level import level
from typing import TYPE_CHECKING, Optional, cast
from pytiling import Tile
from src.utils import bresenham_line

if TYPE_CHECKING:
    from .level_canvas import LevelCanvas


class CanvasClickHandler:
    def __init__(self, canvas: "LevelCanvas"):
        self.canvas = canvas

        self.floor = level.map.tilemap.get_layer("floor")
        self.walls = level.map.tilemap.get_layer("walls")

        self._bind_click_hold_events()

    def _bind_click_hold_events(self):
        self.canvas.bind("<ButtonPress-1>", self._start_click)
        self.canvas.bind("<B1-Motion>", self._on_click_hold)
        self.canvas.bind("<ButtonRelease-1>", self._stop_click)

    def _start_click(self, event):
        """Handle starting a click on the canvas."""
        self.drawn_tile_positions: list[tuple[int, int]] = []
        initial_grid_pos = self._get_grid_position((event.x, event.y))
        if initial_grid_pos:
            self.last_grid_pos = initial_grid_pos
            self._process_single_grid_position(initial_grid_pos)

    def _on_click_hold(self, event):
        """Handle click holding on the canvas by interpolating tiles along the path."""
        current_grid_pos = self._get_grid_position((event.x, event.y))
        if not current_grid_pos:
            return

        if not hasattr(self, "last_grid_pos"):
            self.last_grid_pos = current_grid_pos

        # Generate all grid positions between last and current
        line_positions = bresenham_line(self.last_grid_pos, current_grid_pos)
        for pos in line_positions:
            self._process_single_grid_position(pos)

        self.last_grid_pos = current_grid_pos

    def _stop_click(self, event):
        """Handle stopping a click on the canvas."""
        self.drawn_tile_positions = []
        if hasattr(self, "last_grid_pos"):
            del self.last_grid_pos

    def _get_grid_position(
        self, mouse_position: tuple[int, int]
    ) -> Optional[tuple[int, int]]:
        """Convert mouse coordinates to grid coordinates, adjusting for scroll."""
        x, y = self.canvas.translate_mouse_coords(mouse_position)
        tile_width, tile_height = level.map.tile_size
        grid_x = x // tile_width
        grid_y = y // tile_height
        if level.map.position_is_valid((grid_x, grid_y)):
            return (grid_x, grid_y)

        return None

    def _process_single_grid_position(self, grid_pos: tuple[int, int]):
        """Process a single grid position if it's valid and not already processed."""
        if grid_pos in self.drawn_tile_positions:
            return
        self.drawn_tile_positions.append(grid_pos)

        self.selected_layer_name = level.selector.get_selection("layer")
        self.selected_canvas_object_name = cast(
            str,
            level.selector.get_selection(self.selected_layer_name + ".canvas_object"),
        )
        self.selected_tool_name = level.selector.get_selection("tool")

        self._handle_place_element(grid_pos)

    def _handle_place_element(self, grid_pos: tuple[int, int]):
        if self.selected_tool_name == "pencil":
            level.map.get_layer(
                self.selected_layer_name
            ).canvas_object_manager.get_canvas_object(
                self.selected_canvas_object_name
            ).click_callback(
                grid_pos
            )
        elif self.selected_tool_name == "eraser":
            removed_element = level.map.get_layer(
                self.selected_layer_name
            ).remove_element_at(grid_pos)

            if removed_element is None:
                return
            level.map.tilemap.check_erase(removed_element, self.selected_layer_name)
