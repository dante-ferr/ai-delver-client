import customtkinter as ctk
from level_loader import level_loader
from typing import TYPE_CHECKING
from ._canvas_click_handler import CanvasClickHandler
from ._canvas_scroller import CanvasScroller
from ._canvas_grid_element_renderer import CanvasGridElementRenderer
from ._canvas_overlay import CanvasOverlay
from pytiling import opposite_directions, direction_vectors, Direction

if TYPE_CHECKING:
    from pytiling import Direction, GridMap


class LevelCanvas(ctk.CTkCanvas):
    def __init__(self, parent):
        super().__init__(parent, highlightthickness=0)

        self.configure(bg="black")

        self._zoom_level = 1.0

        self._add_event_listeners()

        self.click_handler = CanvasClickHandler(self)
        self.grid_element_renderer = CanvasGridElementRenderer(self)
        self.overlay = CanvasOverlay(self)
        self.scroller = CanvasScroller(self)

        self.draw_offset: tuple[int, int] = (0, 0)

        self.refresh()

    @property
    def zoom_level(self) -> float:
        """The current magnification level of the canvas."""
        return self._zoom_level

    def set_zoom_level(self, value: float, origin_x: int, origin_y: int):
        """
        Sets the zoom level of the canvas, scaling relative to a given
        origin point (usually the mouse cursor).
        """
        if value <= 0:
            raise ValueError("scale must be positive")
        if abs(value - self._zoom_level) < 1e-9:  # Floating point comparison
            return

        ratio = value / self._zoom_level
        self._zoom_level = value
        
        self.refresh()

    def shift_offset_towards(self, direction: Direction, size: int):
        self.draw_offset = (
            self.draw_offset[0]
            + (direction_vectors[direction][0] * size)
            * level_loader.level.map.tile_size[0],
            self.draw_offset[1]
            + (direction_vectors[direction][1] * size)
            * level_loader.level.map.tile_size[1],
        )

        # self.refresh()

    def _add_event_listeners(self):
        level_loader.level.map.events["expanded"].connect(
            self._expansion_callback, weak=True
        )
        level_loader.level.map.events["reducted"].connect(
            self._reduction_callback, weak=True
        )

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

        if level_loader.level.toggler.vars["grid_lines"].get():
            self.overlay.draw_grid_lines()
        else:
            self.delete("line")
        self.overlay.draw_border()

    def update_draw_order(self):
        """Ensure layers are drawn in the correct Z-index order."""
        layers = level_loader.level.map.layers

        for layer in layers:
            tag = f"layer={layer.name}"
            self.tag_raise(tag)
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
            coords[0] - (self.draw_offset[0] // level_loader.level.map.tile_size[0]),
            coords[1] - (self.draw_offset[1] // level_loader.level.map.tile_size[1]),
        )

    def get_relative_grid_pos(self, coords: tuple[int, int]) -> tuple[int, int]:
        return (
            coords[0] + (self.draw_offset[0] // level_loader.level.map.tile_size[0]),
            coords[1] + (self.draw_offset[1] // level_loader.level.map.tile_size[1]),
        )

    # @property
    # def grid_lines(self):
    #     return level_loader.level.toggler.vars["grid_lines"].get()

    # @property
    # def map_size(self):
    #     return level_loader.level.map.size
    #         coords[0] + (self.draw_offset[0] // level_loader.level.map.tile_size[0]),
    #         coords[1] + (self.draw_offset[1] // level_loader.level.map.tile_size[1]),
    #     )

    @property
    def grid_lines(self):
        return level_loader.level.toggler.vars["grid_lines"].get()

    @property
    def map_size(self):
        return (
            level_loader.level.map.size[0] * self.zoom_level,
            level_loader.level.map.size[1] * self.zoom_level
        )

    @property
    def tile_size(self):
        return (
            level_loader.level.map.tile_size[0] * self.zoom_level,
            level_loader.level.map.tile_size[1] * self.zoom_level,
        )
