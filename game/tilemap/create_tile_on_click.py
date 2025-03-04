from typing import TYPE_CHECKING, Callable
from pyglet.window import mouse
from utils import translate_mouse_coords

if TYPE_CHECKING:
    from pytiling import TilemapLayer, Tile
    from ..camera import Camera
    from pyglet.window import Window


def create_tile_on_click(
    tilemap_layer: "TilemapLayer",
    create_tile_callback: Callable[[int, int], "Tile"],
    camera: "Camera",
    window: "Window",
):
    def on_mouse_press(x, y, button, modifiers):
        world_pos = translate_mouse_coords((x, y), camera, window)

        if button == mouse.LEFT:
            grid_x, grid_y = tilemap_layer.actual_pos_to_tilemap_pos(world_pos)
            tile = create_tile_callback(grid_x, grid_y)
            tilemap_layer.add_tile(tile)

    return on_mouse_press
