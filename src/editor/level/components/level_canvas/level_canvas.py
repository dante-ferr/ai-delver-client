import customtkinter as ctk
from editor.level import level
from typing import TYPE_CHECKING
from ._canvas_click_handler import CanvasClickHandler
from ._canvas_scroller import CanvasScroller
from ._canvas_grid_element_renderer import CanvasGridElementRenderer
from ._canvas_overlay import CanvasOverlay
from pytiling import opposite_directions, direction_vectors, Direction

if TYPE_CHECKING:
    from pytiling import Tile, Direction, GridMap
    from editor.level.grid_map.world_objects_map.world_object import (
        WorldObjectRepresentation,
    )


class LevelCanvas(ctk.CTkCanvas):
    def __init__(self, parent):
        super().__init__(parent, highlightthickness=0)

        self.configure(bg="black")

        self._add_event_listeners()

        self.click_handler = CanvasClickHandler(self)
        self.grid_element_renderer = CanvasGridElementRenderer(self)
        self.overlay = CanvasOverlay(self)
        self.scroller = CanvasScroller(self)

        self.draw_offset: tuple[int, int] = (0, 0)

        self.refresh()

    def shift_offset_towards(self, direction: Direction, size: int):
        self.draw_offset = (
            self.draw_offset[0]
            + (direction_vectors[direction][0] * size) * level.map.tile_size[0],
            self.draw_offset[1]
            + (direction_vectors[direction][1] * size) * level.map.tile_size[1],
        )

    def _add_event_listeners(self):
        level.map.events["expanded"].connect(self._expansion_callback, weak=True)
        level.map.events["reducted"].connect(self._reduction_callback, weak=True)

    def _expansion_callback(
        self,
        sender,
        direction: Direction,
        size: int,
        new_positions: "GridMap.NewPositions",
    ):
        if direction in ("top", "left"):
            self.shift_offset_towards(direction, size)

        self.overlay.handle_expansion(new_positions)
        self._on_map_size_change()

    def _reduction_callback(
        self,
        sender,
        direction: Direction,
        size: int,
        removed_positions: "GridMap.RemovedPositions",
    ):
        self.grid_element_renderer.handle_reduction(removed_positions)
        self.overlay.handle_reduction(removed_positions)

        if direction in ("top", "left"):
            self.shift_offset_towards(opposite_directions[direction], size)

        self._on_map_size_change()

    def _on_map_size_change(self):
        self.overlay.draw_border()

    def refresh(self):
        self.grid_element_renderer.erase_all_grid_elements()
        self.grid_element_renderer.draw_all_grid_elements()

        if level.toggler.vars["grid_lines"].get():
            self.overlay.draw_grid_lines()
        else:
            self.delete("line")
        self.overlay.draw_border()

    def update_draw_order(self):
        """Ensure layers are drawn in the correct Z-index order."""
        layers = level.map.layers

        for layer_name in layers:
            self.tag_raise(f"layer_{layer_name}")
        self.tag_raise("line")
        self.tag_raise("border")

    def items_with_tags(self, *tags):
        """Return a list of items that have all the given tags."""
        if not tags:
            return []

        items_with_all_tags = set(self.find_withtag(tags[0]))

        for tag in tags[1:]:
            items_with_all_tags &= set(self.find_withtag(tag))

        return list(items_with_all_tags)

    def get_absolute_grid_pos(self, coords: tuple[int, int]) -> tuple[int, int]:
        return (
            coords[0] - (self.draw_offset[0] // level.map.tile_size[0]),
            coords[1] - (self.draw_offset[1] // level.map.tile_size[1]),
        )

    def get_relative_grid_pos(self, coords: tuple[int, int]) -> tuple[int, int]:
        return (
            coords[0] + (self.draw_offset[0] // level.map.tile_size[0]),
            coords[1] + (self.draw_offset[1] // level.map.tile_size[1]),
        )

    @property
    def grid_lines(self):
        return level.toggler.vars["grid_lines"].get()

    @property
    def map_size(self):
        return level.map.size
