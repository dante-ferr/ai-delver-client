import pyglet
from ..tilemap import Tilemap


class PygletTilemapRenderer:
    layer_groups: dict[str, pyglet.graphics.Group]

    def __init__(self, tilemap: Tilemap):
        self.tilemap = tilemap

        self.layer_groups = {}

    def assign_group_to_layer(self, layer_name: str, group: pyglet.graphics.Group):
        self.layer_groups[layer_name] = group

    def draw(self):
        tile_width, tile_height = self.tilemap.tileset.tile_size
        for layer in self.tilemap.layers.values():
            group = self.layer_groups[layer.name]

            for tile in layer.grid:
                if tile and tile.display:
                    tile_x, tile_y = tile.position
                    tile_x_pos = tile_x * tile_width
                    tile_y_pos = tile_y * tile_height

                    pyglet.graphics.draw(
                        4,
                        pyglet.gl.GL_QUADS,
                        (
                            "v2f",
                            [
                                tile_x_pos,
                                tile_y_pos,
                                tile_x_pos + tile_width,
                                tile_y_pos,
                                tile_x_pos + tile_width,
                                tile_y_pos + tile_height,
                                tile_x_pos,
                                tile_y_pos + tile_height,
                            ],
                        ),
                        ("c3B", [255, 255, 255] * 4),  # White color for placeholder
                        batch=batch,
                    )  # Add to batch
