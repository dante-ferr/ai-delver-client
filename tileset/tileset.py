class Tileset:
    tile_size: tuple[int, int]

    def __init__(self, tileset_path: str, tile_size: tuple[int, int]):
        self.tileset_path = tileset_path
        self.tile_size = tile_size
