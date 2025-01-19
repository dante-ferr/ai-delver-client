from tileset_manager import Tileset, TilemapLayer, Tilemap, PygletTilemapRenderer
from .groups import floor_layer, walls_layer


def tilemap_factory():
    tileset = Tileset("assets/tilesets/dungeon_tileset.png", (32, 32))
    walls = TilemapLayer("walls", tileset)
    floor = TilemapLayer("floor", tileset)

    tilemap = Tilemap((16, 32))
    tilemap.add_layer(floor)
    tilemap.add_layer(walls)

    tilemap_renderer = PygletTilemapRenderer(tilemap)
    tilemap_renderer.assign_group_to_layer("floor", floor_layer)
    tilemap_renderer.assign_group_to_layer("walls", walls_layer)

    # for position in wall_positions:
    #     wall_tile = AutotileTile(position, "wall")
    #     walls.add_tile(wall_tile, False)

    # walls.format()

    return tilemap_renderer
