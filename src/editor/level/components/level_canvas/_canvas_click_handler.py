from editor.level import level
from typing import TYPE_CHECKING, Optional, cast
from pytiling import Tile
from src.utils import bresenham_line

if TYPE_CHECKING:
    from .level_canvas import LevelCanvas


class CanvasClickHandler:
    def __init__(self, canvas: "LevelCanvas"):
        self.canvas = canvas

        self.floor = level.tilemap.get_layer("floor")
        self.walls = level.tilemap.get_layer("walls")
        # print(f"Floor grid: {self.floor.grid}")
        # print(f"Walls grid: {self.walls.grid}")

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
        tile_width, tile_height = level.tile_size
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

        self.layer_name = level.selector.get_selection("layer")
        self.canvas_object_name = cast(
            str, level.selector.get_selection(self.layer_name + ".canvas_object")
        )
        self.tool_name = level.selector.get_selection("tool")

        if self.layer_name in ("walls", "floor") and self.tool_name in (
            "pencil",
            "eraser",
        ):
            self._handle_place_wall_or_floor(grid_pos)
        else:
            self._handle_place_element(grid_pos)

    def _handle_place_wall_or_floor(
        self,
        grid_pos: tuple[int, int],
    ):
        using_wall_tool = (
            self.layer_name == "walls" and self.canvas_object_name == "wall"
        )
        using_floor_tool = (
            self.layer_name == "floor" and self.canvas_object_name == "floor"
        )

        place_basic_wall = (using_wall_tool and self.tool_name == "pencil") or (
            self.layer_name == "floor" and self.tool_name == "eraser"
        )
        place_basic_floor = (using_floor_tool and self.tool_name == "pencil") or (
            self.layer_name == "walls" and self.tool_name == "eraser"
        )

        if place_basic_wall:
            new_tile = self.walls.canvas_object_manager.get_canvas_object(
                "wall"
            ).click_callback(grid_pos)

            self._reduce_grid_size_if_needed(new_tile)
        elif place_basic_floor:
            new_tile = self.floor.canvas_object_manager.get_canvas_object(
                "floor"
            ).click_callback(grid_pos)

            self._expand_grid_size_if_needed(new_tile)
        else:
            self._handle_place_element(grid_pos)

    def _reduce_grid_size_if_needed(self, new_tile: "Tile"):
        reduced = False
        tile_x, tile_y = new_tile.position

        def _process_line(edge, walls=self.walls, level=level):
            nonlocal reduced

            full_of_walls = all(
                tile is not None and tile.name == "wall"
                for tile in walls.get_edge_tiles(edge, retreat=1)
            )

            if not full_of_walls:
                return
            deleted_elements = level.reduce_towards(edge)
            if not deleted_elements:
                return
            reduced = True

            for layer_name, elements in deleted_elements.items():
                for element in elements:
                    if element is None:
                        continue
                    self.canvas.grid_element_renderer.erase_grid_element(
                        element, layer_name
                    )

        grid_width, grid_height = level.tilemap.grid_size

        if tile_x == 1:
            _process_line("left")
        if tile_x == grid_width - 2:
            _process_line("right")
        if tile_y == 1:
            _process_line("top")
        if tile_y == grid_height - 2:
            _process_line("bottom")

        if reduced:
            self.canvas.refresh()

    def _expand_grid_size_if_needed(self, new_tile: "Tile"):
        if new_tile.edges is None:
            return
        for edge in new_tile.edges:
            added_positions = level.expand_towards(edge)
            if not added_positions:
                continue
            for x, y in added_positions:
                self.walls.create_autotile_tile_at((x, y), "wall")

        self.canvas.refresh()

    def _handle_place_element(self, grid_pos: tuple[int, int]):
        if self.tool_name == "pencil":
            level.get_layer(self.layer_name).canvas_object_manager.get_canvas_object(
                self.canvas_object_name
            ).click_callback(grid_pos)
        elif self.tool_name == "eraser":
            level.get_layer(self.layer_name).remove_element_at(grid_pos)
