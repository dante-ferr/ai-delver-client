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
    """
    The main canvas widget for the level editor.

    This class is the core of the visual editor, responsible for displaying the
    level grid, tiles, objects, and overlays. It manages zooming, scrolling,
    and dispatches events to its various handler components (renderer, click handler,
    scroller, overlay).
    """
    def __init__(self, parent):
        super().__init__(parent, highlightthickness=0)

        self.configure(bg="black")

        self._zoom_level = 1

        self._add_event_listeners()

        # The offset (in grid units) for drawing, used to simulate camera movement.
        self._grid_draw_offset: tuple[int, int] = (0, 0)

        self.click_handler = CanvasClickHandler(self)
        self.grid_element_renderer = CanvasGridElementRenderer(self)
        self.overlay = CanvasOverlay(self)
        self.scroller = CanvasScroller(self)

        self.refresh()

    @property
    def zoom_level(self) -> int:
        """The current magnification level of the canvas."""
        return self._zoom_level

    def set_zoom_level(self, value: int, origin_x: int, origin_y: int):
        """
        Sets the zoom level by re-rendering and repositioning existing canvas items
        relative to a given origin point.
        """
        if value <= 0:
            raise ValueError("Zoom level must be positive")
        if abs(value - self._zoom_level) < 1e-9:
            return

        old_zoom = self._zoom_level
        self._zoom_level = value

        # Rescale and reposition all existing image-based grid elements.
        for item_id in self.find_withtag("grid_element"):
            self.grid_element_renderer.rescale_and_reposition_item(
                item_id, old_zoom, self.zoom_level, origin_x, origin_y
            )

        # Redraw non-image overlays like grid lines and borders
        self.overlay.refresh()

    def _add_event_listeners(self):
        """Binds canvas methods to events from the underlying level map data model."""
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
        """
        Callback for when the level map is expanded. It shifts the drawing offset
        if the expansion is on the top or left, to keep the existing map in place.
        """
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
        """
        Callback for when the level map is reduced. It handles removing visual
        elements and shifting the drawing offset if necessary.
        """
        self.grid_element_renderer.handle_reduction(removed_positions)
        self.overlay.handle_reduction(removed_positions)

        if direction in ("top", "left"):
            self.shift_offset_towards(opposite_directions[direction], size)

        self._on_map_size_change()

    def shift_offset_towards(self, direction: Direction, size: int):
        """Adjusts the grid drawing offset by a given size in a specific direction."""
        self._grid_draw_offset = (
            self._grid_draw_offset[0] + direction_vectors[direction][0] * size,
            self._grid_draw_offset[1] + direction_vectors[direction][1] * size,
        )

    def _on_map_size_change(self):
        self.overlay.draw_border()

    def refresh(self):
        """Performs a full redraw of all canvas elements."""
        self.grid_element_renderer.erase_all_grid_elements()
        self.grid_element_renderer.draw_all_grid_elements()

        self.overlay.refresh()

    def update_draw_order(self):
        """Ensure layers are drawn in the correct Z-index order."""
        layers = level_loader.level.map.layers

        for layer in layers:
            tag = f"layer={layer.name}"
            self.tag_raise(tag)
        self.tag_raise("line")
        self.tag_raise("border")

    def items_with_tags(self, *tags):
        """
        Finds all canvas items that have *all* of the specified tags.
        This is an alternative to `find_withtag` which uses an AND condition
        instead of OR.
        """
        if not tags:
            return []

        items_with_all_tags = set(self.find_withtag(tags[0]))

        for tag in tags[1:]:
            items_with_all_tags &= set(self.find_withtag(tag))

        return list(items_with_all_tags)

    def canvas_to_world_grid_pos(self, coords: tuple[int, int]) -> tuple[int, int]:
        """
        Converts grid coordinates from the canvas's relative space to the
        level map's absolute world space, accounting for the `_grid_draw_offset`.

        Args:
            coords: A tuple (x, y) of the grid position relative to the canvas.

        Returns:
            A tuple (x, y) of the absolute grid position in the world map.
        """
        return (
            coords[0] - self._grid_draw_offset[0],
            coords[1] - self._grid_draw_offset[1],
        )

    def world_to_canvas_grid_pos(self, coords: tuple[int, int]) -> tuple[int, int]:
        """
        Converts grid coordinates from the level map's absolute world space to
        the canvas's relative space, accounting for the `_grid_draw_offset`.

        Args:
            coords: A tuple (x, y) of the absolute grid position in the world map.

        Returns:
            A tuple (x, y) of the grid position relative to the canvas.
        """
        return (
            coords[0] + self._grid_draw_offset[0],
            coords[1] + self._grid_draw_offset[1],
        )

    @property
    def zoomed_draw_offset(self):
        """The drawing offset in pixels, adjusted for the current zoom level."""
        return (
            self._grid_draw_offset[0] * self.tile_size[0],
            self._grid_draw_offset[1] * self.tile_size[1],
        )

    @property
    def draw_offset(self):
        """The drawing offset in pixels, at a zoom level of 1."""
        return (
            self._grid_draw_offset[0] * level_loader.level.map.tile_size[0],
            self._grid_draw_offset[1] * level_loader.level.map.tile_size[1],
        )

    @property
    def grid_lines(self):
        from src.core.state_managers import canvas_state_manager
        """Whether grid lines should be visible, based on the global state."""
        return canvas_state_manager.vars["grid_lines"].get()

    @property
    def map_size(self):
        """The total size of the map in pixels, adjusted for zoom."""
        return (
            level_loader.level.map.size[0] * self.zoom_level,
            level_loader.level.map.size[1] * self.zoom_level
        )

    @property
    def tile_size(self):
        """The current tile size in pixels, adjusted for zoom level."""
        return (
            level_loader.level.map.tile_size[0] * self.zoom_level,
            level_loader.level.map.tile_size[1] * self.zoom_level,
        )
