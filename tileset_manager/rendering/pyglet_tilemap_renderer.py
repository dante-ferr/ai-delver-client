import pyglet
from typing import Any
import numpy as np
from PIL import Image
from ..tilemap_layer import TilemapLayer
from ..tile.tile import Tile


class PygletTilemapRenderer:
    """A helper object that can be used to render a tilemap using pyglet."""

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
        """Assign a group to a layer. This will be used to draw the tiles in the layer in the correct order."""
        self.layer_groups[layer_name] = group

    def _create_tile_images(self):
        """Create a dictionary of numpy 2d arrays of tile images. Each array corresponds to a layer in the tilemap, with the same images as its corresponding tileset."""
        self.tile_images = {}

        for layer in self.tilemap.layers.values():
            if layer.tileset is None:
                raise ValueError("Tileset is not set for layer.")
            tileset_width, tileset_height = layer.tileset.size
            tile_width, tile_height = layer.tileset.tile_size

            self.tile_images[layer.name] = np.empty(
                (tileset_height, tileset_width),
                dtype=pyglet.image.ImageData,
            )

            tile_byte_images = layer.tileset.get_tile_images()

            for x in range(tile_byte_images.shape[1]):
                for y in range(tile_byte_images.shape[0]):
                    byte_data = tile_byte_images[y, x]

                    if byte_data:
                        # self.tile_images[layer.name][y, x] = pyglet.image.ImageData(
                        #     tile_width, tile_height, "RGBA", byte_data
                        # )
                        image_data = Image.frombytes(
                            "RGBA", (tile_width, tile_height), byte_data
                        )
                        image_data = image_data.transpose(Image.FLIP_TOP_BOTTOM)
                        byte_data_flipped = image_data.tobytes()

                        self.tile_images[layer.name][y, x] = pyglet.image.ImageData(
                            tile_width, tile_height, "RGBA", byte_data_flipped
                        )

    def _create_tile_sprites(self):
        """Create a dictionary of numpy 2d arrays of tile sprites. Each array corresponds to a layer in the tilemap."""
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

            for x in range(layer.grid.shape[1]):
                for y in range(layer.grid.shape[0]):
                    tile = layer.grid[y, x]
                    if tile is None:
                        continue
                    if tile.display is None:
                        continue

                    tile_x_pos, tile_y_pos = self.timelap_layer_pos_to_pyglet_pos(
                        tile.position, layer
                    )

                    tile_image = self.tile_images[layer.name][
                        tile.display[1], tile.display[0]
                    ]
                    if tile_image is None:
                        continue

                    tile_sprite = pyglet.sprite.Sprite(
                        tile_image,
                        tile_x_pos,
                        tile_y_pos,
                        batch=self.batch,
                        group=group,
                    )
                    tile_sprite.scale_x = 1
                    tile_sprite.scale_y = 1
                    self.tile_sprites[layer.name][y, x] = tile_sprite

    def create_tile_on_click(self, layer, create_tile_callback: Tile):
        """Create a callback function that can be used to create a tile on click. The output callback must be pushed as a handle of the pyglet window. It takes the grid coordinates of the tile and returns a tile. The tile will be added to the layer and the sprite will be drawn."""

        def on_mouse_press(x, y, button, modifiers):
            if button == pyglet.window.mouse.LEFT:
                grid_x, grid_y = self.pyglet_pos_to_tilemap_layer_pos((x, y), layer)
                tile = create_tile_callback(grid_x, grid_y)
                tile.set_position((grid_x, grid_y))

                self.tilemap.layers["walls"].add_tile(tile)
                self.draw(update_sprites=True)

        return on_mouse_press

    def timelap_layer_pos_to_pyglet_pos(
        self, position: tuple[int, int], layer: TilemapLayer
    ):
        """Convert a tile position in the tilemap layer to a position in the pyglet window."""
        tile_width, tile_height = layer.tileset.tile_size
        map_height = layer.grid.shape[0] * tile_height
        return (position[0] * tile_width, map_height - (position[1] + 1) * tile_height)

    def pyglet_pos_to_tilemap_layer_pos(
        self, position: tuple[int, int], layer: TilemapLayer
    ):
        """Convert a position in the pyglet window to a tile position in the tilemap layer."""
        tile_width, tile_height = layer.tileset.tile_size
        map_height = layer.grid.shape[0] * tile_height
        pos = int(position[0] // tile_width), int(
            (map_height - position[1]) // tile_height
        )
        return pos

    def draw(self, update_sprites: bool = False):
        """Draw the tilemap. If update_sprites is True, the sprites will be updated. Otherwise, they will be created if they don't exist."""
        if update_sprites:
            self._create_tile_sprites()
        elif not self.tile_sprites:
            self._create_tile_sprites()

        self.batch.draw()
