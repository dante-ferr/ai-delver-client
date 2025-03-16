from .level_factory import LevelFactory
from typing import TYPE_CHECKING, Literal, Any, Callable
from .level_selector import LevelSelector
from .level_toggler import LevelToggler
import json
from itertools import chain

if TYPE_CHECKING:
    from .world_objects_map import WorldObjectsMap
    from pytiling import Tilemap

with open("src/config.json", "r") as general_config_data:
    general_config = json.load(general_config_data)

LAYER_ORDER = general_config["layer_order"]


class Level:
    def __init__(
        self,
        tilemap: "Tilemap",
        entity_map: "WorldObjectsMap",
    ):
        self.tilemap = tilemap
        self.entity_map = entity_map

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
        self.entity_map.resize(size)

    @property
    def layers(self):
        """Returns a list of layers in the correct order."""
        layers = []

        for layer_name in LAYER_ORDER:

            if self.tilemap.has_layer(layer_name):
                tilemap_layer = self.tilemap.get_layer(layer_name)
                layers.append(tilemap_layer)
            if self.entity_map.has_layer(layer_name):
                entity_layer = self.entity_map.get_layer(layer_name)
                layers.append(entity_layer)

        return layers

    @property
    def canvas_objects(self):
        return chain.from_iterable(layer.canvas_objects for layer in self.layers)

    def expand_towards(
        self,
        direction: Literal["left", "right", "top", "bottom"],
        size=1,
    ):
        """Expand the grid in the specified direction."""
        self.tilemap.expand_towards(direction, size)
        added_positions = self.entity_map.expand_towards(direction, size)
        return added_positions

    def reduce_towards(
        self, direction: Literal["left", "right", "top", "bottom"], size=1
    ):
        """Reduce the grid in the specified direction."""
        self.tilemap.reduce_towards(direction, size)
        added_positions = self.entity_map.reduce_towards(direction, size)
        return added_positions


level = LevelFactory().level
