from .entity_layer import EntityLayer


class EntityMap:
    def __init__(self, size: tuple[int, int] = (8, 8)):
        self.layers: dict[str, "EntityLayer"] = {}
        self._size = size

    def add_layer(self, layer: "EntityLayer"):
        """Add a entity layer to the map."""
        self.layers[layer.name] = layer

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: tuple[int, int]):
        """Set the size of the entity map. This will resize all layers to match."""
        self._size = size
        for layer in self.layers.values():
            layer.size = size
