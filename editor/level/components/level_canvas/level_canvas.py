import customtkinter as ctk
from editor.level import level
from pytiling import AutotileTile
from editor.level.tilemap import TilesetImage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytiling import Tileset, Tile, TilemapLayer


class LevelCanvas(ctk.CTkCanvas):
    def __init__(self, parent):
        super().__init__(parent, highlightthickness=0)
        self._initialize_tileset_images()
        self.drawn_tiles: dict[tuple[int, int], int] = {}

        self.configure(bg="black")

        self.bind("<Button-1>", self.handle_click)
        self.bind("<ButtonPress-3>", self.start_scroll)
        self.bind("<B3-Motion>", self.on_scroll)
        self.bind("<ButtonRelease-3>", self.stop_scroll)

        self.last_x: int = 0
        self.last_y: int = 0

        self.scrolling = False

        level.tilemap.get_layer("walls").add_format_callback(self._draw_tile)

        self._draw_grid_lines()
        self._draw_borders()

    def _initialize_tileset_images(self):
        """Create a dictionary of numpy 2d arrays of tileset images."""
        self.tileset_images: dict[Tileset, TilesetImage] = {}
        for tileset in level.tilemap.tilesets:
            self.tileset_images[tileset] = TilesetImage(tileset)

    def handle_click(self, event):
        """Handle a click on the canvas."""
        x, y = self._translate_mouse_coords((event.x, event.y))
        grid_x = x // self.tile_size[0]
        grid_y = y // self.tile_size[1]

        self._create_add_tile((grid_x, grid_y))

    def _create_add_tile(self, position: tuple[int, int]):
        """Create a tile at the given position."""
        layer = level.tilemap.get_layer("walls")
        if layer.get_tile(position):
            return
        tile = AutotileTile(position, "wall")
        layer.add_tile(tile)

        self._draw_tile(tile)

    def _draw_tile(self, tile: "Tile"):
        """Draw a tile on the canvas."""
        layer = tile.layer
        if not layer:
            raise ValueError("Tile does not have a layer.")

        grid_x, grid_y = tile.position
        x = grid_x * self.tile_size[0]
        y = grid_y * self.tile_size[1]

        photo_image = self.tileset_images[layer.tileset].get_tile_image(tile.display)

        if (grid_x, grid_y) in self.drawn_tiles:
            self.delete(self.drawn_tiles[(grid_x, grid_y)])
        self.drawn_tiles[(grid_x, grid_y)] = self.create_image(
            x, y, image=photo_image, anchor="nw"
        )

        self._draw_grid_lines()

    def _draw_grid_lines(self):
        """Draw grid lines on the canvas."""
        tile_width, tile_height = self.tile_size
        map_width, map_height = self.map_size

        for x in range(0, map_width, tile_width):
            self.create_line(x, 0, x, map_width, fill="gray")
        for y in range(0, map_height, tile_height):
            self.create_line(0, y, map_height, y, fill="gray")

    def _draw_borders(self):
        """Draw borders on the canvas."""
        map_width, map_height = self.map_size

        self.create_rectangle(0, 0, map_width, map_height, outline="gray", width=2)

    def start_scroll(self, event):
        """Start scrolling when the right mouse button is pressed."""
        self.scrolling = True
        self.scroll_start_x = event.x - self.last_x
        self.scroll_start_y = event.y - self.last_y

    def on_scroll(self, event):
        """Scroll the canvas based on mouse movement."""
        if self.scrolling:
            scroll_x = event.x - self.scroll_start_x
            scroll_y = event.y - self.scroll_start_y
            self.scan_dragto(scroll_x, scroll_y, gain=1)
            self.last_x = scroll_x
            self.last_y = scroll_y

    def _translate_mouse_coords(self, coords: tuple[int, int]) -> tuple[int, int]:
        return (coords[0] - self.last_x, coords[1] - self.last_y)

    def stop_scroll(self, event):
        """Stop scrolling when the right mouse button is released."""
        self.scrolling = False

    @property
    def tile_size(self):
        return level.tilemap.tile_size

    @property
    def map_size(self):
        return level.tilemap.size
