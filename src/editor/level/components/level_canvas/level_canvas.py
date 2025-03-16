import customtkinter as ctk
from editor.level import level
from editor.level.editor_tilemap import TilesetImage
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

        level.tilemap.add_format_callback_to_all_layers(self._handle_tile_format)
        level.tilemap.add_remove_tile_callback_to_all_layers(self._handle_tile_remove)

        level.toggler.set_toggle_callback("grid_lines", self._handle_grid_lines_toggle)

        self.click_handler = CanvasClickHandler(self)
        self.scroller = CanvasScroller(self)

        self.refresh()

    def refresh(self):
        self._draw_all_tiles()
        self._draw_grid_lines()
        self._draw_border()

    def _draw_all_tiles(self):
        """Draw all tiles on the canvas."""
        self.delete("tile")

        for tile in level.tilemap.all_tiles:
            self._draw_tile(tile)

    def _initialize_tileset_images(self):
        """Create a dictionary of numpy 2d arrays of tileset images."""
        self.tileset_images: dict[Tileset, TilesetImage] = {}
        for tileset in level.tilemap.tilesets:
            self.tileset_images[tileset] = TilesetImage(tileset)

    def _handle_tile_format(self, tile: "Tile"):
        """Handle the tile format."""
        self._draw_tile(tile)

    def _handle_tile_remove(self, tile: "Tile", layer_name: str):
        """Handle the tile removal."""
        self.erase_tile(tile.position, layer_name)

    def _draw_tile(self, tile: "Tile"):
        """Draw a tile on the canvas."""
        layer = tile.layer

        grid_x, grid_y = tile.position
        x = grid_x * self.tile_size[0]
        y = grid_y * self.tile_size[1]

        self.erase_tile((grid_x, grid_y), layer.name)

        photo_image = self.tileset_images[layer.tileset].get_tile_image(tile.display)
        position_tag = f"{(grid_x, grid_y)}"
        layer_tag = f"layer_{layer.name}"
        self.create_image(
            x, y, image=photo_image, anchor="nw", tags=(position_tag, layer_tag, "tile")
        )

        self._update_draw_order()

    def _update_draw_order(self):
        """Ensure layers are drawn in the correct Z-index order."""
        layers = level.layers

        for layer_name in layers:
            self.tag_raise(f"layer_{layer_name}")
        self.tag_raise("line")
        self.tag_raise("border")

    def erase_tile(self, tile_position: tuple[int, int], layer_name: str):
        """Erase a tile from the canvas only if it has both the position and layer tags."""
        position_tag = f"{tile_position[0],tile_position[1]}"
        layer_tag = f"layer_{layer_name}"

        items_with_both_tags = set(self.find_withtag(position_tag)) & set(
            self.find_withtag(layer_tag)
        )

        for item in items_with_both_tags:
            self.delete(item)

    def _handle_grid_lines_toggle(self, value: bool):
        """Handle the grid lines toggle."""
        if value:
            self._draw_grid_lines()
        else:
            self.delete("line")

    def _draw_grid_lines(self):
        """Draw grid lines on the canvas with inverted axes."""
        self.delete("line")

        tile_width, tile_height = self.tile_size
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
        return level.size
