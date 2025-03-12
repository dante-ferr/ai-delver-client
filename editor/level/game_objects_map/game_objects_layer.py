from pytiling import GridLayer


class GameObjectsLayer(GridLayer):
    def __init__(self, name: str, tile_size: tuple[int, int]):
        super().__init__(name, tile_size)
