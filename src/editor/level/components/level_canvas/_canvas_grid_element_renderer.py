from ._tileset_image import TilesetImage
from typing import Literal, TYPE_CHECKING, cast
import customtkinter as ctk
from editor.level import level_loader
from ._world_objects_image import WorldObjectsImage


if TYPE_CHECKING:
    from pytiling import Tileset, Tile, GridElement, GridMap
    from editor.level.grid_map.world_objects_map.world_object import (
        WorldObjectRepresentation,
    )
    from .level_canvas import LevelCanvas


class CanvasGridElementRenderer:
    def __init__(self, canvas: "LevelCanvas"):
        self.canvas = canvas

        self._add_event_listeners()

        self._initialize_tileset_images()
        self.world_objects_image = WorldObjectsImage()

    def _add_event_listeners(self):
        level_loader.level.map.tilemap.on_layer_event(
            "element_created", self._handle_tile_created
        )
        level_loader.level.map.tilemap.on_layer_event(
            "tile_formatted", self._handle_tile_formatted
        )

        level_loader.level.map.on_layer_event(
            "element_removed", self._handle_element_removed
        )

        level_loader.level.map.world_objects_map.on_layer_event(
            "element_created", self._handle_world_object_created
        )
        pass

    def _handle_tile_created(self, sender, element: "GridElement"):
        self.draw_tile(cast("Tile", element))

    def _handle_tile_formatted(self, sender, tile: "Tile"):
        self.draw_tile(tile)

    def _handle_element_removed(self, sender, element: "GridElement", layer_name: str):
        self.erase_grid_element(element, layer_name)

    def _handle_world_object_created(self, sender, element: "GridElement"):
        self.draw_world_object(cast("WorldObjectRepresentation", element))

    def _initialize_tileset_images(self):
        """Create a dictionary of numpy 2d arrays of tileset images."""
        self.tileset_images: dict[Tileset, TilesetImage] = {}
        for tileset in level_loader.level.map.tilemap.tilesets:
            self.tileset_images[tileset] = TilesetImage(tileset)

    def handle_reduction(self, removed_positions: "GridMap.RemovedPositions"):
        for position in removed_positions:
            relative_position = self.canvas.get_relative_grid_pos(position)
            self.canvas.delete(f"position={relative_position}")

    def erase_all_grid_elements(self):
        """Erase all tiles on the canvas."""
        self.canvas.delete("grid_element")

    def draw_all_grid_elements(self):
        """Draw all tiles on the canvas."""
        for tile in level_loader.level.map.tilemap.all_tiles:
            self.draw_tile(tile)
        for world_object in level_loader.level.map.world_objects_map.all_world_objects:
            self.draw_world_object(world_object)

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
        canvas_grid_x, canvas_grid_y = self.canvas.get_relative_grid_pos(
            element.position
        )
        x = canvas_grid_x * level_loader.level.map.tile_size[0]
        y = canvas_grid_y * level_loader.level.map.tile_size[1]

        self.erase_grid_element(element=element)

        self.canvas.create_image(
            x, y, image=image, anchor="nw", tags=self._get_grid_element_tags(element)
        )

        self.canvas.update_draw_order()

    def erase_grid_element(
        self,
        element: "GridElement",
        layer_name: str | Literal["element's"] = "element's",
    ):
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
        canvas_grid_x, canvas_grid_y = self.canvas.get_relative_grid_pos(
            element.position
        )

        position_tag = f"position={(canvas_grid_x, canvas_grid_y)}"
        if layer_name == "element's":
            layer = element.layer
            layer_tag = f"layer={layer.name}"
        else:
            layer_tag = f"layer={layer_name}"

        element_name_tag = f"element_{element.__class__.__name__}"
        grid_element_tag = "grid_element"

        return (position_tag, layer_tag, element_name_tag, grid_element_tag)
