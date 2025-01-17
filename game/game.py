import json
import pyglet
from game.controls import Controls
import pymunk
from typing import Any
from .entities.player import Player
from .tilemap_renderer import get_tilemap_renderer
from .camera import Camera

with open("game/config.json", "r") as file:
    config_data = json.load(file)

global_scale = config_data["global_scale"]
window_width = config_data["window_width"]
window_height = config_data["window_height"]

zoom_level = 1


class Game:
    entities: list[Any] = []

    def __init__(self):
        self.window = pyglet.window.Window()
        self.window.set_size(window_width, window_height)

        self.camera = Camera(self.window)
        self.camera.zoom = zoom_level

        self.space = pymunk.Space()
        self.space.gravity = (0, 0)

        # Initialize player
        player = Player(self.space)
        self.entities.append(player)
        self.player = player

        # player.set_position(
        #     window_width / 2, window_height / 2
        # )
        # player.set_scale(config_data["global_scale"], config_data["global_scale"])
        player.set_angle(180)

        self.tilemap_renderer = get_tilemap_renderer()

        self.keys = pyglet.window.key.KeyStateHandler()
        self.window.push_handlers(self.keys)

    def update(self, dt):
        controls = Controls(self.keys, self.player)
        controls.update(dt)

        self.window.clear()

        self.camera.begin()

        self.tilemap_renderer.draw()
        self.player.update(dt)

    def run(self):
        pyglet.clock.schedule_interval(
            self.update, 1 / float(config_data["fps"])
        )  # Update at 60 FPS
        pyglet.app.run()
