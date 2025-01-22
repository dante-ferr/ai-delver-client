import json
import pyglet
from game.controls import Controls
from typing import Any
from .entities.player import Player
from .tilemap_factory import tilemap_factory
from .camera import Camera
from tileset_manager import AutotileTile
import game.groups as groups
from .space import space

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

        # Initialize player
        player = Player(space=space)
        self.entities.append(player)
        self.player = player

        # player.set_position(
        #     window_width / 2, window_height / 2
        # )
        # player.set_scale(config_data["global_scale"], config_data["global_scale"])
        player.set_angle(180)

        self.tilemap_renderer = tilemap_factory()

        self.keys = pyglet.window.key.KeyStateHandler()
        self.controls = Controls(self.keys, self.player)

        def collision_handler(arbiter, space, data):
            print("Collision Detected!")
            player_shape = arbiter.shapes[0]
            line_shape = arbiter.shapes[1]

            print(f"Player position: {player_shape.body.position}")
            print(f"Line position: {line_shape.body.position}")

            return True

        handler = space.add_collision_handler(1, 2)
        handler.begin = collision_handler

        def create_tile_callback(grid_x, grid_y):
            tile = AutotileTile((grid_x, grid_y), "wall")
            return tile

        self.window.push_handlers(
            self.keys,
            self.tilemap_renderer.create_tile_on_click(
                self.tilemap_renderer.tilemap.layers["walls"], create_tile_callback
            ),
        )

    def update(self, dt):
        self.controls.update(dt)

        self.window.clear()

        self.camera.begin()

        self.tilemap_renderer.draw()

        pyglet.shapes.Line(
            0,
            0,
            100,
            100,
            thickness=2,
            color=(255, 0, 0),
            group=groups.debug,
        ).draw()

        self.player.update(dt)

    def run(self):
        pyglet.clock.schedule_interval(
            self.update, 1 / float(config_data["fps"])
        )  # Update at 60 FPS
        pyglet.app.run()
