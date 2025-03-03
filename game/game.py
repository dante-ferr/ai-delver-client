import json
import pyglet
from game.controls import Controls
from typing import Any
from .entities.player import Player
from .tilemap_factory import tilemap_factory
from .camera import Camera, CenteredCamera
from .space import space
from pytiling import AutotileTile
from pytiling.pyglet_support import create_tile_on_click

with open("game/config.json", "r") as file:
    config_data = json.load(file)

global_scale = config_data["global_scale"]
window_width = config_data["window_width"]
window_height = config_data["window_height"]


class Game:
    entities: list[Any] = []

    def __init__(self):
        self.window = pyglet.window.Window()
        self.window.set_size(window_width, window_height)

        self.camera = CenteredCamera(self.window, min_zoom=0.5, max_zoom=2)

        # Initialize player
        player = Player(space=space)
        self.entities.append(player)
        self.player = player
        player.set_angle(180)

        # Initialize tilemap
        self.tilemap_renderer = tilemap_factory()

        # Initialize controls
        self.keys = pyglet.window.key.KeyStateHandler()
        self.controls = Controls(self.keys)
        self.controls.append_player(player)
        self.controls.append_camera(self.camera)

        def create_tile_callback(grid_x, grid_y):
            tile = AutotileTile((grid_x, grid_y), "wall")
            return tile

        self.window.push_handlers(
            self.keys,
            create_tile_on_click(
                self.tilemap_renderer.layer_renderers["walls"], create_tile_callback
            ),
            on_mouse_scroll=self.controls.on_mouse_scroll,
        )

    def update(self, dt):
        self.window.clear()

        self.tilemap_renderer.render_layer("walls")
        self.player.update(dt)

        self.controls.update(dt)

        with self.camera:
            self.camera.zoom = 1  # 0.75

        space.step(dt)

    def run(self):
        pyglet.clock.schedule_interval(
            self.update, 1 / float(config_data["fps"])
        )  # Update at 60 FPS
        pyglet.app.run()
