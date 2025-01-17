import json
from tileset_manager import (
    Tileset,
    TilemapLayer,
    Tilemap,
    PygletTilemapRenderer,
    Tile,
    AutotileTile,
)
from .groups import floor_layer, walls_layer

# with open("game/config.json", "r") as file:
#     config_data = json.load(file)


def get_tilemap_renderer():
    tileset = Tileset("assets/tilesets/dungeon_tileset.png", (32, 32))
    walls = TilemapLayer("floor", tileset)
    floor = TilemapLayer("walls", tileset)

    tilemap = Tilemap((32, 32))
    tilemap.add_layer(floor)
    tilemap.add_layer(walls)

    tilemap_renderer = PygletTilemapRenderer(tilemap)
    tilemap_renderer.assign_group_to_layer("floor", floor_layer)
    tilemap_renderer.assign_group_to_layer("walls", walls_layer)

    wall_positions = [
        # Fully Surrounded (Center)
        (5, 5),  # Center tile
        # Edges (One neighbor)
        (4, 5),  # Top edge
        (6, 5),  # Bottom edge
        (5, 4),  # Left edge
        (5, 6),  # Right edge
        # Corners (Two neighbors)
        (4, 4),  # Top-left corner
        (4, 6),  # Top-right corner
        (6, 4),  # Bottom-left corner
        (6, 6),  # Bottom-right corner
        # T-junctions (Three neighbors)
        (3, 5),  # T-junction top
        (5, 7),  # T-junction right
        (7, 5),  # T-junction bottom
        (5, 3),  # T-junction left
        # Inner Corners (Three neighbors, more complex)
        (2, 2),  # Inner top-left
        (2, 8),  # Inner top-right
        (8, 2),  # Inner bottom-left
        (8, 8),  # Inner bottom-right
        # Inner T-Junctions (Six neighbors)
        (3, 4),  # Inner T-junction top
        (7, 4),  # Inner T-junction bottom
        (4, 3),  # Inner T-junction left
        (4, 7),  # Inner T-junction right
        (6, 4),  # Inner cross, fully connected
        # Cross (Fully connected to all sides)
        (5, 5),  # Cross (center), all sides connected
        # Straight Edges (Two neighbors, different directions)
        (4, 5),  # Horizontal edge (left-right)
        (5, 4),  # Vertical edge (top-bottom)
        # More specific corner variations:
        (3, 3),  # Inner top-left corner with more complex neighboring
        (7, 3),  # Inner top-right corner with more complex neighboring
        (3, 7),  # Inner bottom-left corner with more complex neighboring
        (7, 7),  # Inner bottom-right corner with more complex neighboring
        # Lone tile (No neighbors)
        (10, 10),  # Lone tile with no neighbors
    ]

    for position in wall_positions:
        wall_tile = AutotileTile(position, "wall")
        walls.add_tile(wall_tile, False)

    walls.format()

    return tilemap_renderer
