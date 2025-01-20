from tileset_manager import (
    Tileset,
    TilemapLayer,
    Tilemap,
    PygletTilemapRenderer,
    TilemapBorderTracer,
)
from .groups import floor_layer, walls_layer

# Criação do tilemap:
# - Criar tileset
# - Criar camadas do tilemap
# - Criar tilemap
# - Adicionar camadas ao tilemap

# Renderização:
# - Criar tilemap renderer (pyglet)
# - Atribuir grupos às camadas do tilemap
# - Renderizar o tilemap por meio do renderer


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

    border_tracer = TilemapBorderTracer(walls)
    border_tracer.add_debug_callback(
        lambda tile: tilemap_renderer.create_debug_lines(border_tracer, walls_layer)
    )

    # for position in wall_positions:
    #     wall_tile = AutotileTile(position, "wall")
    #     walls.add_tile(wall_tile, False)

    # walls.format()

    return tilemap_renderer
