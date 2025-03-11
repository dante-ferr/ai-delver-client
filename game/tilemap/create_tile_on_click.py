from typing import TYPE_CHECKING, Callable
from pyglet.window import mouse

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
        world_pos = camera.translate_mouse_coords((x, y))

        if button == mouse.LEFT:
            grid_x, grid_y = tilemap_layer.actual_pos_to_tilemap_pos(world_pos)
            tile = create_tile_callback(grid_x, grid_y)
            tilemap_layer.add_tile(tile)

    return on_mouse_press
