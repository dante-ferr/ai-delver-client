import pyglet
from typing import Any
import numpy as np


class PygletTilemapRenderer:
    layer_groups: dict[str, pyglet.graphics.Group]
    # Both tile_images and tile_sprites are dictionaries, where the keys are the layer names and the values are numpy arrays of the tile images.
    tile_images: dict[str, np.ndarray[tuple[int, int], Any]]
    tile_sprites: dict[str, np.ndarray[tuple[int, int], Any]]

    def __init__(self, tilemap):
        self.tilemap = tilemap

        self.layer_groups = {}
        self.tile_sprites = {}

        self._create_tile_images()

    def assign_group_to_layer(self, layer_name: str, group: pyglet.graphics.Group):
        self.layer_groups[layer_name] = group

    def _create_tile_images(self):
        self.tile_images = {}

        for layer in self.tilemap.layers.values():
            tileset_width, tileset_height = layer.tileset.size
            tile_width, tile_height = layer.tileset.tile_size

            self.tile_images[layer.name] = np.empty(
                (tileset_width, tileset_height),
                dtype=pyglet.image.ImageData,
            )

            tile_byte_images = layer.tileset.get_tile_images()

            for x in range(tile_byte_images.shape[0]):
                for y in range(tile_byte_images.shape[1]):
                    byte_data = tile_byte_images[x, y]

                    if byte_data:
                        self.tile_images[layer.name][x, y] = pyglet.image.ImageData(
                            tile_width, tile_height, "RGBA", byte_data
                        )

    def _create_tile_sprites(self):
        self.tile_sprites = {}
        self.batch = pyglet.graphics.Batch()

        for layer in self.tilemap.layers.values():
            tile_width, tile_height = layer.tileset.tile_size

            if layer.name not in self.layer_groups:
                raise ValueError(f"Layer '{layer.name}' not assigned to a group.")
            group = self.layer_groups[layer.name]

            self.tile_sprites[layer.name] = np.empty(
                (layer.grid.shape[0], layer.grid.shape[1]),
                dtype=pyglet.sprite.Sprite,
            )

            for x in range(layer.grid.shape[0]):
                for y in range(layer.grid.shape[1]):
                    tile = layer.grid[x, y]
                    if tile is None:
                        continue

                    tile_x_pos = x * tile_width
                    tile_y_pos = y * tile_height

                    print(tile_x_pos, tile_y_pos)

                    tile_image = self.tile_images[layer.name][*tile.display]
                    if tile_image is None:
                        continue

                    tile_sprite = pyglet.sprite.Sprite(
                        tile_image,
                        tile_x_pos,
                        tile_y_pos,
                        batch=self.batch,
                        group=group,
                    )
                    self.tile_sprites[layer.name][x, y] = tile_sprite

    def draw(self, update_sprites: bool = False):
        # The update happens if update_sprites is True, or if there are no tile sprites
        if update_sprites:
            self._create_tile_sprites()
        elif not self.tile_sprites:
            self._create_tile_sprites()

        self.batch.draw()
