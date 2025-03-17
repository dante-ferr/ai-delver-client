from .level_factory import LevelFactory
from typing import TYPE_CHECKING, Literal, Any, Callable
from .level_selector import LevelSelector
from .level_toggler import LevelToggler
import json
from functools import cached_property

if TYPE_CHECKING:
    from .grid_map.world_objects_map import WorldObjectsMap
    from .grid_map.editor_tilemap import EditorTilemap
    from src.editor.level.canvas_object import CanvasObject
    from editor.level.grid_map.editor_tilemap.editor_tilemap_layer import (
        EditorTilemapLayer,
    )
    from editor.level.grid_map.world_objects_map.world_objects_layer.world_objects_layer import (
        WorldObjectsLayer,
    )

with open("src/config.json", "r") as general_config_data:
    general_config = json.load(general_config_data)

LAYER_ORDER = general_config["layer_order"]


class Level:
    def __init__(
        self,
        tilemap: "EditorTilemap",
        world_objects_map: "WorldObjectsMap",
    ):
        self.tilemap = tilemap
        self.world_objects_map = world_objects_map

        self.selector = LevelSelector()
        self.toggler = LevelToggler()

    @property
    def size(self):
        tile_width, tile_height = self.tilemap.tile_size
        return (
            self.grid_size[1] * tile_width,
            self.grid_size[0] * tile_height,
        )

    @property
    def grid_size(self):
        return self.tilemap.grid_size

    @grid_size.setter
    def grid_size(self, size: tuple[int, int]):
        self.tilemap.resize(size)
        self.world_objects_map.resize(size)

    @property
    def tile_size(self):
        return self.tilemap.tile_size

    @cached_property
    def layers(self):
        """Returns a list of layers in the correct order."""
        layers: list["WorldObjectsLayer | EditorTilemapLayer"] = []

        for layer_name in LAYER_ORDER:

            if self.tilemap.has_layer(layer_name):
                tilemap_layer = self.tilemap.get_layer(layer_name)
                layers.append(tilemap_layer)
            if self.world_objects_map.has_layer(layer_name):
                entity_layer = self.world_objects_map.get_layer(layer_name)
                layers.append(entity_layer)

        return layers

    @cached_property
    def _layers_dict(self):
        """Returns a dictionary of all the layers."""
        layers: dict[str, "WorldObjectsLayer | EditorTilemapLayer"] = {}
        for layer in self.layers:
            layers[layer.name] = layer
        return layers

    def get_layer(self, layer_name: str) -> "WorldObjectsLayer | EditorTilemapLayer":
        """Returns a layer by its name."""
        return self._layers_dict[layer_name]

    @property
    def canvas_objects(self):
        canvas_objects: dict[str, "CanvasObject"] = {}

        for layer in self.layers:
            for canvas_object in layer.canvas_object_manager.canvas_objects.values():
                canvas_objects[canvas_object.name] = canvas_object

        return canvas_objects

    def get_canvas_object(self, canvas_object_name: str) -> "CanvasObject":
        return self.canvas_objects[canvas_object_name]

    def expand_towards(
        self,
        direction: Literal["left", "right", "top", "bottom"],
        size=1,
    ):
        """Expand the grid in the specified direction."""
        self.tilemap.expand_towards(direction, size)
        added_positions = self.world_objects_map.expand_towards(direction, size)
        return added_positions

    def reduce_towards(
        self, direction: Literal["left", "right", "top", "bottom"], size=1
    ):
        """Reduce the grid in the specified direction."""
        deleted_tiles = self.tilemap.reduce_towards(direction, size)
        deleted_entities = self.world_objects_map.reduce_towards(direction, size)
        return (deleted_tiles or {}) | (deleted_entities or {})


level = LevelFactory().level
