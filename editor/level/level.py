from .level_factory import LevelFactory
from typing import TYPE_CHECKING
from .level_selector import LevelSelector
from .level_toggler import LevelToggler
import json
from itertools import chain

if TYPE_CHECKING:
    from .world_objects_map import WorldObjectsMap
    from pytiling import Tilemap

with open("config.json", "r") as general_config_data:
    general_config = json.load(general_config_data)

LAYER_ORDER = general_config["layer_order"]


class Level:
    def __init__(self, tilemap: "Tilemap", entity_map: "WorldObjectsMap"):
        self.tilemap = tilemap
        self.entity_map = entity_map

        self.selector = LevelSelector()
        self.toggler = LevelToggler()

    @property
    def grid_size(self):
        return self.tilemap.grid_size

    @grid_size.setter
    def grid_size(self, size: tuple[int, int]):
        self.tilemap.grid_size = size
        self.entity_map.grid_size = size

    @property
    def layers(self):
        """Returns a list of layers in the correct order."""
        layers = []

        for layer_name in LAYER_ORDER:
            tilemap_layer = self.tilemap.get_layer(layer_name)
            entity_layer = self.entity_map.get_layer(layer_name)

            if tilemap_layer is not None:
                layers.append(tilemap_layer)
            if entity_layer is not None:
                layers.append(entity_layer)

        return layers

    @property
    def canvas_objects(self):
        return chain.from_iterable(layer.canvas_objects for layer in self.layers)


level = LevelFactory().level
