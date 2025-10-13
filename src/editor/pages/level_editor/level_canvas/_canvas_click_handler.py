from typing import TYPE_CHECKING, Optional, cast
from src.utils import bresenham_line
from level_loader import level_loader
from pytiling import Tile
from ..level_editor_manager import level_editor_manager

if TYPE_CHECKING:
    from .level_canvas import LevelCanvas


class CanvasClickHandler:
    def __init__(self, canvas: "LevelCanvas"):
        self.canvas = canvas

        self.platforms = level_loader.level.map.tilemap.get_layer("platforms")

        self.drawn_tile_positions: list[tuple[int, int]] = []

        self._bind_click_hold_events()

    def _bind_click_hold_events(self):
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())
        self.canvas.bind("<ButtonPress-1>", self._start_click)
        self.canvas.bind("<B1-Motion>", self._on_click_hold)
        self.canvas.bind("<ButtonRelease-1>", self._stop_click)
        self.canvas.bind("<KeyPress-i>", self._debug_inspect_tile)

    def _start_click(self, event):
        """Handle starting a click on the canvas."""
        self.drawn_tile_positions = []
        initial_canvas_grid_pos = self._get_canvas_grid_position((event.x, event.y))
        if initial_canvas_grid_pos:
            self.last_canvas_grid_pos = initial_canvas_grid_pos
            self._process_single_canvas_grid_position(initial_canvas_grid_pos)

    def _on_click_hold(self, event):
        """Handle click holding on the canvas by interpolating tiles along the path."""
        current_canvas_grid_pos = self._get_canvas_grid_position((event.x, event.y))
        if not current_canvas_grid_pos:
            return

        if not hasattr(self, "last_canvas_grid_pos"):
            self.last_canvas_grid_pos = current_canvas_grid_pos

        # Generate all grid positions between last and current
        line_positions = bresenham_line(
            self.last_canvas_grid_pos, current_canvas_grid_pos
        )
        for pos in line_positions:
            if level_loader.level.map.position_is_valid(
                self.canvas.canvas_to_world_grid_pos(pos)
            ):
                self._process_single_canvas_grid_position(pos)

        self.last_canvas_grid_pos = current_canvas_grid_pos

    def _stop_click(self, event):
        """Handle stopping a click on the canvas."""
        self.drawn_tile_positions = []
        if hasattr(self, "last_canvas_grid_pos"):
            del self.last_canvas_grid_pos

    def _get_canvas_grid_position(
        self, mouse_position: tuple[int, int]
    ) -> Optional[tuple[int, int]]:
        """Convert mouse coordinates to grid coordinates, adjusting for scroll."""
        canvas_x = self.canvas.canvasx(mouse_position[0])
        canvas_y = self.canvas.canvasy(mouse_position[1])
        tile_width, tile_height = level_loader.level.map.tile_size
        canvas_grid_x = int(canvas_x // (tile_width * self.canvas.zoom_level))
        canvas_grid_y = int(canvas_y // (tile_height * self.canvas.zoom_level))

        return (canvas_grid_x, canvas_grid_y)

    def _process_single_canvas_grid_position(self, canvas_grid_pos: tuple[int, int]):
        """Process a single grid position if it's valid and not already processed."""
        if canvas_grid_pos in self.drawn_tile_positions:
            return
        self.drawn_tile_positions.append(canvas_grid_pos)

        self.selected_layer_name = level_editor_manager.selector.get_selection("layer")
        self.selected_canvas_object_name = cast(
            str,
            level_editor_manager.selector.get_selection(
                self.selected_layer_name + ".canvas_object"
            ),
        )
        self.selected_tool_name = level_editor_manager.selector.get_selection("tool")

        grid_pos = self.canvas.canvas_to_world_grid_pos(canvas_grid_pos)
        self._handle_interaction(grid_pos)

    def _handle_interaction(self, grid_pos: tuple[int, int]):
        if not level_loader.level.map.position_is_valid(grid_pos):
            return

        if self.selected_tool_name == "pencil":
            canvas_object = level_editor_manager.objects_manager.get_canvas_object(
                self.selected_canvas_object_name
            )
            canvas_object.create_element_callback(grid_pos)

        elif self.selected_tool_name == "eraser":
            layer = level_loader.level.map.get_layer(self.selected_layer_name)
            canvas_object = level_editor_manager.objects_manager.get_canvas_object(
                self.selected_canvas_object_name
            )

            if canvas_object.remove_element_callback is None:
                removed_element = layer.remove_element_at(grid_pos)
            else:
                removed_element = canvas_object.remove_element_callback(grid_pos)

            if removed_element is None:
                return

    def _debug_inspect_tile(self, event):
        """
        Debug function to print properties of a tile when 'i' is pressed
        over it. Currently prints the tile's display property.
        """
        canvas_grid_pos = self._get_canvas_grid_position((event.x, event.y))
        if not canvas_grid_pos:
            print("DEBUG: No canvas grid position found")
            return

        grid_pos = self.canvas.canvas_to_world_grid_pos(canvas_grid_pos)

        if not level_loader.level.map.position_is_valid(grid_pos):
            print("DEBUG: Invalid grid position")
            return

        selected_layer_name = level_editor_manager.selector.get_selection("layer")
        layer = level_loader.level.map.get_layer(selected_layer_name)

        if not layer:
            print(f"DEBUG: No layer found with name '{selected_layer_name}'")
            return

        element = layer.get_element_at(grid_pos)

        if isinstance(element, Tile):
            tile = cast(Tile, element)
            print(
                f"DEBUG: Tile at {grid_pos} on layer '{layer.name}': display={tile.display}"
            )
