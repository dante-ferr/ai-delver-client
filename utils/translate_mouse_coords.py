from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyglet.window import Window
    from ..game.camera import Camera


def translate_mouse_coords(
    coords: tuple[float, float], camera: "Camera", window: "Window"
):
    x, y = coords
    camera_x, camera_y = camera.position

    translated_x = (-camera_x + x) * camera._zoom + (window.width / 2) * (
        1 - camera._zoom
    )
    translated_y = (-camera_y + y) * camera._zoom + (window.height / 2) * (
        1 - camera._zoom
    )

    return (translated_x, translated_y)
