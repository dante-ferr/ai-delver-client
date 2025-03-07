import customtkinter as ctk
from editor.level import level
from pytiling import AutotileTile
from editor.level.tilemap import TilesetImage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytiling import Tileset


class LevelCanvas(ctk.CTkCanvas):
    def __init__(self, parent):
        super().__init__(parent)
        self._initialize_tileset_images()

        self.drawn_tiles: dict[tuple[int, int], int] = {}

        self.bind("<Button-1>", self.handle_click)

        self._draw_grid_lines()

    def _initialize_tileset_images(self):
        """Create a dictionary of numpy 2d arrays of tileset images."""
        self.tileset_images: dict[Tileset, TilesetImage] = {}
        for tileset in level.tilemap.tilesets:
            self.tileset_images[tileset] = TilesetImage(tileset)

    def handle_click(self, event):
        grid_x = event.x // self.tile_size[0]
        grid_y = event.y // self.tile_size[1]

        layer = level.tilemap.get_layer("walls")
        tile = AutotileTile((grid_x, grid_y), "wall")
        layer.add_tile(tile)

        photo_image = self.tileset_images[layer.tileset].get_tile_image(tile.display)

        x = grid_x * self.tile_size[0]
        y = grid_y * self.tile_size[1]

        if (grid_x, grid_y) in self.drawn_tiles:
            self.delete(self.drawn_tiles[(grid_x, grid_y)])
        self.drawn_tiles[(grid_x, grid_y)] = self.create_image(
            x, y, image=photo_image, anchor="nw"
        )

    def _draw_grid_lines(self):
        """Draw grid lines on the canvas."""
        tile_width, tile_height = self.tile_size
        map_width, map_height = self.map_size

        for x in range(0, map_width, tile_width):
            self.create_line(x, 0, x, map_width, fill="gray")
        for y in range(0, map_height, tile_height):
            self.create_line(0, y, map_height, y, fill="gray")

    @property
    def tile_size(self):
        return level.tilemap.tile_size

    @property
    def map_size(self):
        return level.tilemap.size
