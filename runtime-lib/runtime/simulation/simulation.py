from .. import Runtime
import json
from os import path
from .delver_action import DelverAction

with open(path.join(path.dirname(__file__), "../config.json"), "r") as file:
    config = json.load(file)

DT = 1 / config["fps"] * 3


class Simulation(Runtime):
    def __init__(self, level):
        super().__init__(level, render=False)

        self.elapsed_time = 0.0
        self.delver_actions: list[DelverAction] = []

    def step(self, action: DelverAction):
        self.add_delver_action(action)

        if action["move"]:
            self.delver.move(DT, action["move_angle"])

        reward = 100 if self.delver.check_collision(self.goal) else -1
        ended = reward == 100

        self.update(DT)
        return reward, ended, self.elapsed_time

    def update(self, dt):
        super().update(dt)

        self.elapsed_time += dt

    def add_delver_action(self, action: DelverAction):
        self.delver_actions.append(DelverAction(**action))
