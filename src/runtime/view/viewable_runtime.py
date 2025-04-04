import json
from .. import Runtime
from pyglet_dragonbones import config as pdb_config
from .camera import Camera, Camera
from pyglet.window import Window
from .view_controls import ViewControls
import pyglet

with open("src/runtime/config.json", "r") as file:
    runtime_config_data = json.load(file)

pdb_config.fps = runtime_config_data["fps"]


class ViewableRuntime(Runtime):
    def __init__(self):
        self.camera: None | Camera = None
        self._window: Window | None = pyglet.window.Window(
            fullscreen=False, resizable=False
        )

        super().__init__()

        def _maximize_callback(dt):
            self.window.maximize()
            pyglet.clock.schedule_once(self._on_screen_maximize_interval, 0.01)

        pyglet.clock.schedule_once(_maximize_callback, 0.1)

        self.keys = pyglet.window.key.KeyStateHandler()
        self._create_controls()
        self.window.push_handlers(
            self.keys,
            on_close=self._on_window_close,
        )

    def _create_controls(self):
        self.controls = ViewControls(self.keys)
        self.controls.append_delver(self.delver)

    def _on_screen_maximize_interval(self, dt):
        self._lock_window_size()

        self.camera = Camera(self.window, start_zoom=1, min_zoom=0.25, max_zoom=2)
        self.camera.start_following(self.delver)

        self.controls.append_camera(self.camera)
        self.window.push_handlers(on_mouse_scroll=self.controls.on_mouse_scroll)

    def _on_window_close(self):
        from app_manager import app_manager

        app_manager.stop_game()
        pyglet.clock.schedule_once(lambda dt: self._safe_close(), 0)

        return pyglet.event.EVENT_HANDLED

    def _lock_window_size(self):
        """Locks the window size completely (even on Linux)"""
        width, height = self.window.width, self.window.height

        self.window.set_minimum_size(width, height)
        self.window.set_maximum_size(width, height)
        self.window.set_size(width, height)

        @self.window.event
        def on_resize(new_width, new_height):
            if new_width != width or new_height != height:
                self.window.set_size(width, height)
            return pyglet.event.EVENT_HANDLED

    def update(self, dt):
        self.window.clear()

        self.tilemap_renderer.render_all_layers()
        self.world_objects_controller.draw_world_objects(dt)

        self.controls.update(dt)

        if self.camera is not None:
            with self.camera:
                pass

        super().update(dt)

    def run(self):
        super().run()

        pyglet.clock.schedule_interval(
            self.update, 1 / float(runtime_config_data["fps"])
        )  # Update at 60 FPS
        pyglet.app.run()

    def stop(self):
        super().stop()

        pyglet.clock.unschedule(self.update)

        if self.window:
            self.window.close()

        pyglet.app.exit()

    @property
    def window(self) -> Window:
        if self._window is None:
            raise RuntimeError("Window not initialized")
        return self._window

    @window.setter
    def window(self, window: Window | None):
        self._window = window

    def _safe_close(self):
        """Called in main thread after all drawing completes"""
        if self.window:
            self.window.set_visible(False)

            self.window.remove_handlers()
            self.window.close()
            self.window = None
