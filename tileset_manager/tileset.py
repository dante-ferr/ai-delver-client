from PIL import Image
import numpy as np


class Tileset:
    tile_size: tuple[int, int]

    def __init__(self, tileset_path: str, tile_size: tuple[int, int]):
        self.atlas_image = Image.open(tileset_path)
        self.tile_size = tile_size

        tile_width, tile_height = self.tile_size
        self.size = (
            self.atlas_image.size[0] // tile_width,
            self.atlas_image.size[1] // tile_height,
        )

    def get_tile_images(self):
        tile_images = np.empty(
            (self.size[0], self.size[1]),
            dtype=bytes,
        )

        x = 0
        y = 0
        tile_width, tile_height = self.tile_size

        while x < self.atlas_image.width:
            while y < self.atlas_image.height:
                tile_images[x, y] = self.atlas_image.crop(
                    (x, y, x + tile_width, y + tile_height)
                ).tobytes()

                y += tile_height
            x += tile_width

        return tile_images

    # def get_tile_image(self, tile_position: tuple[int, int]) -> bytes:
    #     return self.tile_images[tile_position]
