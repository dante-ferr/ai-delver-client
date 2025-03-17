from editor.level.grid_map.editor_tilemap import TilesetImage
from typing import Literal, TYPE_CHECKING
import customtkinter as ctk
from editor.level import level
from editor.level.grid_map.world_objects_map import (
    WorldObjectsImage,
)

if TYPE_CHECKING:
    from pytiling import Tileset, Tile, GridElement
    from editor.level.grid_map.world_objects_map.world_object import (
        WorldObjectRepresentation,
    )
    from .level_canvas import LevelCanvas


class CanvasGridElementRenderer:
    def __init__(self, canvas: "LevelCanvas"):
        self.canvas = canvas

        self._initialize_tileset_images()
        self.world_objects_image = WorldObjectsImage()

    def _initialize_tileset_images(self):
        """Create a dictionary of numpy 2d arrays of tileset images."""
        self.tileset_images: dict[Tileset, TilesetImage] = {}
        for tileset in level.tilemap.tilesets:
            self.tileset_images[tileset] = TilesetImage(tileset)

    def erase_all_grid_elements(self):
        """Erase all tiles on the canvas."""
        self.canvas.delete("grid_element")

    def draw_all_grid_elements(self):
        """Draw all tiles on the canvas."""
        for tile in level.tilemap.all_tiles:
            self.draw_tile(tile)

    def draw_tile(self, tile: "Tile"):
        """Draw a tile on the canvas."""
        self._draw_grid_element(
            tile, self.tileset_images[tile.layer.tileset].get_tile_image(tile.display)
        )

    def draw_world_object(self, world_object: "WorldObjectRepresentation"):
        """Draw a world object on the canvas"""
        ctk_image = self.world_objects_image.get_image(world_object.name)
        self._draw_grid_element(world_object, ctk_image)

    def _draw_grid_element(self, element: "GridElement", image: "ctk.CTkImage | None"):
        """Draw a grid element on the canvas"""
        layer = element.layer
        grid_x, grid_y = element.position
        x = grid_x * level.tile_size[0]
        y = grid_y * level.tile_size[1]

        self.erase_grid_element(element, layer.name)

        self.canvas.create_image(
            x, y, image=image, anchor="nw", tags=self._get_grid_element_tags(element)
        )

        self.canvas.update_draw_order()

    def erase_grid_element(self, element: "GridElement", layer_name: str):
        """Erase a grid element from the canvas only if it has both the position and layer tags."""
        for item in self.canvas.items_with_tags(
            *self._get_grid_element_tags(element, layer_name)
        ):
            self.canvas.delete(item)

    def _get_grid_element_tags(
        self,
        element: "GridElement",
        layer_name: str | Literal["element's"] = "element's",
    ):
        """Return the tag for a grid element."""
        grid_x, grid_y = element.position

        position_tag = f"{(grid_x, grid_y)}"
        if layer_name == "element's":
            layer = element.layer
            layer_tag = f"layer_{layer.name}"
        else:
            layer_tag = f"layer_{layer_name}"

        element_name_tag = f"element_{element.__class__.__name__}"
        grid_element_tag = "grid_element"

        return (position_tag, layer_tag, element_name_tag, grid_element_tag)
