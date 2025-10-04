from ._tileset_image import TilesetImage
from typing import Literal, TYPE_CHECKING, cast
from level_loader import level_loader
from ._world_objects_image import WorldObjectsImage
from pytiling import Tile
from level.grid_map.world_objects_map.world_object import (
    WorldObjectRepresentation,
)
from PIL import ImageTk, Image

if TYPE_CHECKING:
    from pytiling import Tileset, GridElement, GridMap
    from PIL.ImageTk import PhotoImage
    from .level_canvas import LevelCanvas


class CanvasGridElementRenderer:
    def __init__(self, canvas: "LevelCanvas"):
        self.canvas = canvas

        self._add_event_listeners()

        self.photo_image_cache: dict[int, ImageTk.PhotoImage] = {}
        self._initialize_tileset_images()
        self.world_objects_image = WorldObjectsImage()

    def _add_event_listeners(self):
        level_loader.level.map.tilemap.on_layer_event(
            "element_created", self._handle_tile_created
        )
        level_loader.level.map.tilemap.on_layer_event(
            "tile_formatted", self._handle_tile_formatted
        )
        level_loader.level.map.tilemap.on_layer_event(
            "element_removed", self._handle_element_removed
        )

        level_loader.level.map.world_objects_map.on_layer_event(
            "element_created", self._handle_world_object_created
        )
        level_loader.level.map.world_objects_map.on_layer_event(
            "element_removed", self._handle_element_removed
        )

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
        pil_image = self.world_objects_image.get_image(world_object.canvas_object_name)
        self._draw_grid_element(world_object, pil_image)

    def _draw_grid_element(self, element: "GridElement", pil_image: "Image.Image | None"):
        """Draw a grid element on the canvas, applying zoom and offset."""
        if pil_image is None:
            return

        tile_width, tile_height = level_loader.level.map.tile_size

        scaled_width = int(tile_width * self.canvas.zoom_level)
        scaled_height = int(tile_height * self.canvas.zoom_level)

        # Use a simple cache key. id(pil_image) is a good candidate.
        cache_key = id(pil_image)
        photo_image = self.photo_image_cache.get(cache_key)

        # If the image is not in cache or its size has changed, create a new one.
        if (
            photo_image is None
            or photo_image.width() != scaled_width
            or photo_image.height() != scaled_height
        ):
            resized_image = pil_image.resize((scaled_width, scaled_height), Image.NEAREST)
            photo_image = ImageTk.PhotoImage(resized_image)
            self.photo_image_cache[cache_key] = photo_image

        # Calculate screen coordinates using zoom and offset
        # The absolute grid position is the "world" coordinate
        world_x = element.position[0] * tile_width
        world_y = element.position[1] * tile_height

        # Apply offset, then zoom
        screen_x = (world_x + self.canvas.draw_offset[0]) * self.canvas.zoom_level
        screen_y = (world_y + self.canvas.draw_offset[1]) * self.canvas.zoom_level

        self.erase_grid_element(element=element)

        self.canvas.create_image(
            screen_x,
            screen_y,
            image=photo_image,
            anchor="nw",
            tags=self._get_grid_element_tags(element),
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
        # We use the absolute grid position for a stable ID during resizes/pans
        position_tag = f"grid_pos={element.position}"
        if layer_name == "element's":
            layer = element.layer
            layer_tag = f"layer={layer.name}"
        else:
            layer_tag = f"layer={layer_name}"

        grid_element_tag = "grid_element"

        return (position_tag, layer_tag, grid_element_tag)

    def _get_image_for_element(self, element: "GridElement") -> "Image.Image | None":
        """Helper to get the correct image for any grid element."""
        if isinstance(element, Tile):
            tile = cast("Tile", element)
            return self.tileset_images[element.layer.tileset].get_tile_image(tile.display)
        elif isinstance(element, WorldObjectRepresentation):
            world_object = cast("WorldObjectRepresentation", element)
            return self.world_objects_image.get_image(world_object.canvas_object_name)
        return None
