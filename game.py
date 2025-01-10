import json
import pyglet
from pyglet.window import key
from game.entities.skeleton.skeleton import Skeleton
import game.groups as groups

with open("config.json", 'r') as file:
    config_data = json.load(file)

class Game:
    def __init__(self):
        self.window = pyglet.window.Window()
        self.window.set_size(config_data["window_width"], config_data["window_height"])

        # Initialize skeleton
        self.skeleton = Skeleton("assets/sprites/delver", groups.delver)
        self.skeleton.set_position(config_data["window_width"] / 2, config_data["window_height"] / 2)
        self.skeleton.set_scale(3, 3)
        self.skeleton.set_angle(180)

        # Register the key press event
        self.keys = pyglet.window.key.KeyStateHandler()
        self.window.push_handlers(self.keys)

    def update(self, dt):
        self.window.clear()
        if self.keys[key.LEFT]:
            self.skeleton.set_angle(self.skeleton.angle - 2)
        elif self.keys[key.RIGHT]:
            self.skeleton.set_angle(self.skeleton.angle + 2)
        self.skeleton.draw()

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60.0)  # Update at 60 FPS
        pyglet.app.run()

game = Game()
game.run()
