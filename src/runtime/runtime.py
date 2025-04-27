import json
from .level_setup import tilemap_renderer_factory
from pyglet_dragonbones import config as pdb_config
from .level_setup import world_objects_controller_factory
from typing import cast
from .world_objects.entities.delver import Delver
from .space import space
import time

with open("src/runtime/config.json", "r") as file:
    config_data = json.load(file)

pdb_config.fps = config_data["fps"]


class Runtime:
    def __init__(self):
        self.running = False

        self.world_objects_controller = world_objects_controller_factory(space)
        self.delver = cast(
            "Delver", self.world_objects_controller.get_world_object("delver")
        )
        self.goal = self.world_objects_controller.get_world_object("goal")

        self.tilemap_renderer = tilemap_renderer_factory()

    def update(self, dt):
        self.world_objects_controller.update_world_objects(dt)
        # self._check_collisions()

        space.step(dt)

    # def _check_collisions(self):
    #     if self.delver.check_collision(self.goal):
    #         from app_manager import app_manager

    #         app_manager.stop_game()

    def run(self):
        self.running = True

    def stop(self):
        if not self.running:
            return

        self.running = False

    @property
    def tilemap(self):
        return self.tilemap_renderer.tilemap
