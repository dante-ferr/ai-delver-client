import json
import pyglet
from game.entities.skeleton.skeleton import Skeleton
import game.groups as groups
from game.controls import Controls

# from pymunk import pyglet_util, Space

with open("game/config.json", "r") as file:
    config_data = json.load(file)


class Game:
    def __init__(self):
        self.window = pyglet.window.Window()
        self.window.set_size(config_data["window_width"], config_data["window_height"])

        # self.space = Space()
        # self.space.gravity = (0, 0)

        # Initialize skeleton
        self.skeleton = Skeleton("assets/sprites/delver", groups.delver)
        self.skeleton.set_position(
            config_data["window_width"] / 2, config_data["window_height"] / 2
        )
        self.skeleton.set_scale(2, 2)
        self.skeleton.set_angle(180)
        self.skeleton.set_animation("run")

        # Register the key press event
        self.keys = pyglet.window.key.KeyStateHandler()
        self.window.push_handlers(self.keys)

    def update(self, dt):
        self.window.clear()
        controls = Controls(self.keys)
        controls.update(dt)
        self.skeleton.update(dt)

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)  # Update at 60 FPS
        pyglet.app.run()
