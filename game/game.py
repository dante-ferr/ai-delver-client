import json
import pyglet
from game.controls import Controls
from typing import Any
from .entities.player.player import Player
from .tilemap.tilemap_factory import tilemap_factory
from .camera import Camera, Camera
from .space import space
from pytiling import AutotileTile
from .tilemap.create_tile_on_click import create_tile_on_click
from utils import refine_texture

with open("game/config.json", "r") as file:
    config_data = json.load(file)

global_scale = config_data["global_scale"]
window_width = config_data["window_width"]
window_height = config_data["window_height"]


class Game:
    entities: list[Any] = []

    def __init__(self):
        self.window = pyglet.window.Window(window_width, window_height, resizable=False)

        # Initialize player
        player = Player(space=space)
        player.set_angle(180)
        player.position = (window_width / 2, window_height / 2)
        self.player = player
        self.entities.append(player)

        # Initialize camera
        self.camera = Camera(self.window, start_zoom=0.5, min_zoom=0.25, max_zoom=2)
        self.camera.start_following(player)

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
                self.tilemap_renderer.tilemap.get_layer("walls"),
                create_tile_callback,
                self.camera,
                self.window,
            ),
            on_mouse_scroll=self.controls.on_mouse_scroll,
        )

    def update(self, dt):
        self.window.clear()

        self.tilemap_renderer.render_layer("walls")
        self.player.update(dt)
        self.controls.update(dt)

        with self.camera:
            pass

        space.step(dt)

    def run(self):
        pyglet.clock.schedule_interval(
            self.update, 1 / float(config_data["fps"])
        )  # Update at 60 FPS
        pyglet.app.run()
