from .tilemap_layer import TilemapLayer
from .tileset import Tileset


class Tilemap:
    layer_names: list[str]
    layers: dict[str, TilemapLayer]

    default_size = (8, 8)

    def __init__(self, tileset: Tileset):
        self.tileset = tileset

        self.layer_names = []
        self.layers = {}

        self.set_size(self.default_size)

    def add_layer(self, layer_index: int, layer_name: str):
        layer = TilemapLayer(layer_name, self.size)
        self.layers[layer_name] = layer
        self.layer_names.insert(layer_index, layer_name)

    def set_size(self, size: tuple[int, int]):
        self.size = size
        for layer in self.layers.values():
            layer.set_size(size)
