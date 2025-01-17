from tileset_manager import (
    Tileset,
    TilemapLayer,
    Tilemap,
    PygletTilemapRenderer,
    Tile,
    AutotileTile,
)
from .groups import floor_layer, walls_layer


def get_tilemap_renderer():
    tileset = Tileset("assets/tilesets/dungeon_tileset.png", (32, 32))
    walls = TilemapLayer("floor", tileset)
    floor = TilemapLayer("walls", tileset)

    tilemap = Tilemap()
    tilemap.add_layer(floor)
    tilemap.add_layer(walls)

    tilemap_renderer = PygletTilemapRenderer(tilemap)
    tilemap_renderer.assign_group_to_layer("floor", floor_layer)
    tilemap_renderer.assign_group_to_layer("walls", walls_layer)

    wall_positions = [
        # Fully surrounded (center)
        (5, 5),
        # Edges
        (4, 5),  # Top edge
        (6, 5),  # Bottom edge
        (5, 4),  # Left edge
        (5, 6),  # Right edge
        # Corners
        (4, 4),  # Top-left corner
        (4, 6),  # Top-right corner
        (6, 4),  # Bottom-left corner
        (6, 6),  # Bottom-right corner
        # T-junctions
        (3, 5),  # T-junction top
        (5, 7),  # T-junction right
        (7, 5),  # T-junction bottom
        (5, 3),  # T-junction left
        # Inner corners
        (2, 2),  # Inner top-left
        (2, 8),  # Inner top-right
        (8, 2),  # Inner bottom-left
        (8, 8),  # Inner bottom-right
        # Lone tile
        (10, 10),
    ]

    for position in wall_positions:
        wall_tile = AutotileTile(position, "wall")
        walls.add_tile(wall_tile, False)

    walls.format()

    return tilemap_renderer
