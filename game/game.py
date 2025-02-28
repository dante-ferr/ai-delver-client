import json
import pyglet
from game.controls import Controls
from typing import Any
from .entities.player import Player
from .tilemap_factory import tilemap_factory
from .camera import Camera, CenteredCamera
import game.groups as groups
from .space import space
from pytiling import AutotileTile


with open("game/config.json", "r") as file:
    config_data = json.load(file)

global_scale = config_data["global_scale"]
window_width = config_data["window_width"]
window_height = config_data["window_height"]

zoom_level = 3


class Game:
    entities: list[Any] = []

    def __init__(self):
        self.window = pyglet.window.Window()
        self.window.set_size(window_width, window_height)

        self.camera = CenteredCamera(self.window)
        self.camera.zoom = zoom_level

        # Initialize player
        player = Player(space=space)
        self.entities.append(player)
        self.player = player
        player.set_angle(180)

        # Initialize tilemap
        self.tilemap_renderer = tilemap_factory()

        def create_tile_callback(grid_x, grid_y):
            tile = AutotileTile((grid_x, grid_y), "wall")
            return tile

        # Initialize controls
        self.keys = pyglet.window.key.KeyStateHandler()
        self.controls = Controls(self.keys, self.player)

        self.window.push_handlers(
            self.keys,
            self.tilemap_renderer.create_tile_on_click(
                self.tilemap_renderer.tilemap.layers["walls"], create_tile_callback
            ),
        )

    def update(self, dt):
        self.controls.update(dt)

        self.camera.position = self.player.position

        self.window.clear()
        self.tilemap_renderer.draw()

        self.player.update(dt)

        self.camera.begin()
        self.camera.end()

        space.step(dt)

    def run(self):
        pyglet.clock.schedule_interval(
            self.update, 1 / float(config_data["fps"])
        )  # Update at 60 FPS
        pyglet.app.run()
