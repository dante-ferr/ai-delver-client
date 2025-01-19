from pyglet import window
from typing import TYPE_CHECKING
from pymunk import Vec2d
import math
from utils.vector_to_angle import vector_to_angle

if TYPE_CHECKING:
    from .entities.skeleton.skeleton import Skeleton


class Controls:
    keys: window.key.KeyStateHandler

    def __init__(self, keys: window.key.KeyStateHandler, player: "Skeleton"):
        self.keys = keys
        self.player = player

    def update(self, dt):
        self._update_player_controls(dt)

    def _update_player_controls(self, dt):
        run_vector = [0, 0]
        if self.keys[window.key.LEFT]:
            run_vector[0] = -1
        if self.keys[window.key.RIGHT]:
            run_vector[0] = 1
        if self.keys[window.key.UP]:
            run_vector[1] = -1
        if self.keys[window.key.DOWN]:
            run_vector[1] = 1

        if run_vector == [0, 0]:
            self.player.animation_run(None)
            self.player.body.set_velocity(Vec2d(0, 0))
        else:
            run_velocity = [
                run_vector[0] * self.player.speed,
                run_vector[1] * self.player.speed,
            ]
            self.player.set_target_angle(vector_to_angle(run_vector) - 90)
            self.player.update_angle_to_target(dt)
            self.player.animation_run("run")

            magnitude = math.sqrt(run_velocity[0] ** 2 + run_velocity[1] ** 2)
            if magnitude > self.player.speed:
                run_velocity[0] *= self.player.speed / magnitude
                run_velocity[1] *= self.player.speed / magnitude

            self.player.body.set_velocity(Vec2d(run_velocity[0], -run_velocity[1]))
