import customtkinter as ctk
from editor.level import level
from editor.level.tilemap import TilesetImage
from typing import TYPE_CHECKING
from .canvas_click_handler import CanvasClickHandler
from .canvas_scroller import CanvasScroller

if TYPE_CHECKING:
    from pytiling import Tileset, Tile


class LevelCanvas(ctk.CTkCanvas):
    def __init__(self, parent):
        super().__init__(parent, highlightthickness=0)
        self._initialize_tileset_images()

        self.configure(bg="black")

        level.tilemap.add_format_callback_to_all_layers(self._draw_tile)
        level.tilemap.add_remove_tile_callback_to_all_layers(self._erase_tile)
        walls_layer = level.tilemap.get_layer("walls")
        if walls_layer:
            walls_layer.formatter.format_all_tiles()

        level.toggler.set_toggle_callback("grid_lines", self._handle_grid_lines_toggle)

        self.click_handler = CanvasClickHandler(self)
        self.scroller = CanvasScroller(self)

        self._draw_grid_lines()
        self._draw_borders()

    def _initialize_tileset_images(self):
        """Create a dictionary of numpy 2d arrays of tileset images."""
        self.tileset_images: dict[Tileset, TilesetImage] = {}
        for tileset in level.tilemap.tilesets:
            self.tileset_images[tileset] = TilesetImage(tileset)

    def _draw_tile(self, tile: "Tile"):
        """Draw a tile on the canvas."""
        layer = tile.layer

        grid_x, grid_y = tile.position
        x = grid_x * self.tile_size[0]
        y = grid_y * self.tile_size[1]

        photo_image = self.tileset_images[layer.tileset].get_tile_image(tile.display)

        self.create_image(x, y, image=photo_image, anchor="nw", tags=f"{x},{y}")

        if self.grid_lines:
            self._draw_grid_lines()

    def _erase_tile(self, tile: "Tile"):
        """Erase a tile from the canvas."""
        self.delete(f"{tile.position[0]},{tile.position[1]}")

    def _handle_grid_lines_toggle(self, value: bool):
        """Handle the grid lines toggle."""
        if value:
            self._draw_grid_lines()
        else:
            self._delete_grid_lines()

    def _draw_grid_lines(self):
        """Draw grid lines on the canvas."""
        self._delete_grid_lines()

        tile_width, tile_height = self.tile_size
        map_width, map_height = self.map_size

        for x in range(0, map_width, tile_width):
            self.create_line(x, 0, x, map_width, fill="gray", tags="grid")
        for y in range(0, map_height, tile_height):
            self.create_line(0, y, map_height, y, fill="gray", tags="grid")

    def _delete_grid_lines(self):
        """Delete grid lines from the canvas."""
        self.delete("grid")

    def _draw_borders(self):
        """Draw borders on the canvas."""
        map_width, map_height = self.map_size

        self.create_rectangle(0, 0, map_width, map_height, outline="gray", width=2)

    def translate_mouse_coords(self, coords: tuple[int, int]) -> tuple[int, int]:
        return (coords[0] - self.scroller.last_x, coords[1] - self.scroller.last_y)

    @property
    def grid_lines(self):
        return level.toggler.vars["grid_lines"].get()

    @property
    def tile_size(self):
        return level.tilemap.tile_size

    @property
    def map_size(self):
        return level.tilemap.size
