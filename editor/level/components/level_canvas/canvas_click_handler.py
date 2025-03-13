from editor.level import level
from typing import TYPE_CHECKING, Optional
from pytiling import Tile, AutotileTile
from .canvas_scroller import CanvasScroller
from utils import bresenham_line

if TYPE_CHECKING:
    from .level_canvas import LevelCanvas


class CanvasClickHandler:
    def __init__(self, canvas: "LevelCanvas"):
        self.canvas = canvas
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
        tile_width, tile_height = self.canvas.tile_size
        grid_x = x // tile_width
        grid_y = y // tile_height
        if level.tilemap.position_is_valid((grid_x, grid_y)):
            return (grid_x, grid_y)
        return None

    def _process_single_grid_position(self, grid_pos: tuple[int, int]):
        """Process a single grid position if it's valid and not already processed."""
        if grid_pos in self.drawn_tile_positions:
            return
        self.drawn_tile_positions.append(grid_pos)

        layer_name = level.selector.get_selection("layer")
        tool_name = level.selector.get_selection("tool")
        canvas_object = level.selector.get_selection(layer_name + ".canvas_object")

        using_wall_tool = layer_name == "walls" and canvas_object == "wall"
        using_floor_tool = layer_name == "floor" and canvas_object == "floor"

        place_autotile_wall = (using_wall_tool and tool_name == "pencil") or (
            using_floor_tool and tool_name == "eraser"
        )
        place_floor = (using_floor_tool and tool_name == "pencil") or (
            using_wall_tool and tool_name == "eraser"
        )

        if place_autotile_wall:
            tile = AutotileTile(position=grid_pos, autotile_object="wall")
            self._add_tile(tile, "walls")
        elif place_floor:
            tile = Tile(position=grid_pos, display=(0, 0))
            self._add_tile(tile, "floor")

    def _add_tile(self, tile: "Tile", layer_name: str):
        """Add a tile to a tilemap layer."""
        layer = level.tilemap.get_layer(layer_name)
        if layer:
            layer.add_tile(tile)

    def _remove_tile(self, tile: "Tile", layer_name: str):
        """Remove a tile from a tilemap layer."""
        layer = level.tilemap.get_layer(layer_name)
        if layer:
            layer.remove_tile(tile)
