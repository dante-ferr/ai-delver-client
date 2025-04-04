from pytiling import (
    TilemapBorderTracer,
    PymunkTilemapPhysics,
)
from pytiling.pyglet_support import TilemapRenderer
from ..space import space
from level import level_loader


def tilemap_renderer_factory():
    walls = level_loader.level.map.tilemap.get_layer("walls")
    border_tracer = TilemapBorderTracer(walls)
    PymunkTilemapPhysics(border_tracer, space)

    tilemap_renderer = TilemapRenderer(level_loader.level.map.tilemap)
    return tilemap_renderer
