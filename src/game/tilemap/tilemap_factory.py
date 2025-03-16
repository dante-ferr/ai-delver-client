from pytiling import (
    Tileset,
    TilemapLayer,
    Tilemap,
    TilemapBorderTracer,
    PymunkTilemapPhysics,
)
from pytiling.pyglet_support import TilemapRenderer
from ..space import space

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
    tileset = Tileset("assets/img/tilesets/dungeon/walls.png")
    walls = TilemapLayer("walls", tileset)
    floor = TilemapLayer("floor", tileset)

    tilemap = Tilemap((640, 640), (32, 32))
    tilemap.add_layer(floor)
    tilemap.add_layer(walls)

    tilemap_renderer = TilemapRenderer(tilemap)

    border_tracer = TilemapBorderTracer(walls)

    border_tracer.add_create_tile_callback(
        lambda tile: tilemap_renderer.update_debug_lines(border_tracer)
    )
    tilemap_physics = PymunkTilemapPhysics(border_tracer, space)

    # walls.format()

    return tilemap_renderer
