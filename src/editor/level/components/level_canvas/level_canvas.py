import customtkinter as ctk
from editor.level import level
from typing import TYPE_CHECKING
from ._canvas_click_handler import CanvasClickHandler
from ._canvas_scroller import CanvasScroller
from ._canvas_grid_element_renderer import CanvasGridElementRenderer

if TYPE_CHECKING:
    from pytiling import Tile
    from editor.level.grid_map.world_objects_map.world_object import (
        WorldObjectRepresentation,
    )


class LevelCanvas(ctk.CTkCanvas):
    def __init__(self, parent):
        super().__init__(parent, highlightthickness=0)

        self.configure(bg="black")

        level.tilemap.add_format_callback_to_all_layers(self._handle_tile_format)
        level.tilemap.add_create_element_callback_to_all_layers(
            self._handle_tile_create
        )
        level.tilemap.add_remove_element_callback_to_all_layers(
            self._handle_tile_remove
        )
        level.world_objects_map.add_create_element_callback_to_all_layers(
            self._handle_world_object_create
        )
        level.world_objects_map.add_remove_element_callback_to_all_layers(
            self._handle_world_object_remove
        )

        level.toggler.set_toggle_callback("grid_lines", self._handle_grid_lines_toggle)

        self.grid_element_renderer = CanvasGridElementRenderer(self)

        self.click_handler = CanvasClickHandler(self)
        self.scroller = CanvasScroller(self)

        self.refresh()

    def refresh(self):
        self.grid_element_renderer.erase_all_grid_elements()
        self.grid_element_renderer.draw_all_grid_elements()

        if level.toggler.vars["grid_lines"].get():
            self._draw_grid_lines()
        else:
            self.delete("line")
        self._draw_border()

    def _handle_tile_format(self, tile: "Tile"):
        """Handle the tile format."""
        self.grid_element_renderer.draw_tile(tile)

    def _handle_tile_create(self, tile: "Tile"):
        """Handle the tile format."""
        self.grid_element_renderer.draw_tile(tile)

    def _handle_tile_remove(self, tile: "Tile", layer_name: str):
        """Handle the tile removal."""
        self.grid_element_renderer.erase_grid_element(tile, layer_name)

    def _handle_world_object_create(self, entity: "WorldObjectRepresentation"):
        """Handle the world object creation."""
        self.grid_element_renderer.draw_world_object(entity)

    def _handle_world_object_remove(
        self, entity: "WorldObjectRepresentation", layer_name: str
    ):
        """Handle the world object removal."""
        self.grid_element_renderer.erase_grid_element(entity, layer_name)

    def update_draw_order(self):
        """Ensure layers are drawn in the correct Z-index order."""
        layers = level.layers

        for layer_name in layers:
            self.tag_raise(f"layer_{layer_name}")
        self.tag_raise("line")
        self.tag_raise("border")

    def _handle_grid_lines_toggle(self, value: bool):
        """Handle the grid lines toggle."""
        if value:
            self._draw_grid_lines()
        else:
            self.delete("line")

    def _draw_grid_lines(self):
        """Draw grid lines on the canvas with inverted axes."""
        self.delete("line")

        tile_width, tile_height = level.tile_size
        map_width, map_height = self.map_size

        for x in range(0, map_width, tile_width):
            self.create_line(0, x, map_height, x, fill="gray", tags="line")
        for y in range(0, map_height, tile_height):
            self.create_line(y, 0, y, map_width, fill="gray", tags="line")

    def _draw_border(self):
        """Draw borders on the canvas."""
        self.delete("border")

        map_width, map_height = self.map_size
        self.create_rectangle(
            0, 0, map_height, map_width, outline="gray", width=2, tags="border"
        )

    def items_with_tags(self, *tags):
        """Return a list of items that have all the given tags."""
        if not tags:
            return []

        items_with_all_tags = set(self.find_withtag(tags[0]))

        for tag in tags[1:]:
            items_with_all_tags &= set(self.find_withtag(tag))

        return list(items_with_all_tags)

    def translate_mouse_coords(self, coords: tuple[int, int]) -> tuple[int, int]:
        return (coords[0] - self.scroller.last_x, coords[1] - self.scroller.last_y)

    @property
    def grid_lines(self):
        return level.toggler.vars["grid_lines"].get()

    @property
    def map_size(self):
        return level.size
