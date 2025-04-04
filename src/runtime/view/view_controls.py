from pyglet import window
from typing import TYPE_CHECKING
from utils import vector_to_angle

if TYPE_CHECKING:
    from ..world_objects.entities.delver import Delver


class ViewControls:
    keys: window.key.KeyStateHandler

    def __init__(self, keys: window.key.KeyStateHandler):
        self.keys = keys

    def append_camera(self, camera):
        self.camera = camera

    def append_delver(self, delver: "Delver"):
        self.delver = delver

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self._handle_zoom(scroll_y)

    def _handle_zoom(self, scroll_y):
        if not self.camera:
            raise ValueError("Camera not set")
        zoom_speed = 0.1
        self.camera.zoom = self.camera.zoom + scroll_y * zoom_speed

    def update(self, dt):
        pass
