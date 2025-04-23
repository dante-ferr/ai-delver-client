from .. import Runtime
from typing import Any
from .delver_action import DelverAction


class Simulation(Runtime):
    def __init__(self):
        super().__init__()

        self.elapsed_time = 0.0
        self.delver_actions: list[DelverAction] = []

    def update(self, dt):
        super().update(dt)

        self.elapsed_time += dt

    def add_delver_action(self, action: DelverAction):
        self.delver_actions.append(DelverAction(**action))
