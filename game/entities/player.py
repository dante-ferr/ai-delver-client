import pyglet
from pyglet_dragonbones.skeleton import Skeleton
from pyglet_dragonbones.skeleton_body import SkeletonBody
import json
import pymunk
from pymunk import Vec2d
from utils import angle_to_vector
import math

with open("game/config.json", "r") as file:
    config_data = json.load(file)

window_width = config_data["window_width"]
window_height = config_data["window_height"]

delver_groups = {
    "head": pyglet.graphics.Group(3),
    "left_foot": pyglet.graphics.Group(0),
    "right_foot": pyglet.graphics.Group(0),
    "body": pyglet.graphics.Group(1),
    "left_hand": pyglet.graphics.Group(2),
    "right_hand": pyglet.graphics.Group(2),
}


class Player(Skeleton):
    run_speed = 200
    is_running = False
    run_angle = 0.0

    def __init__(self, space: pymunk.Space):
        mass = 1
        radius = 10
        player_body = SkeletonBody(
            mass=mass, moment=pymunk.moment_for_circle(mass, 0, radius)
        )
        shape = pymunk.Circle(player_body, radius)
        shape.collision_type = 1
        space.add(player_body, shape)

        player_body.setup_collision_handlers()
        player_body.position = pymunk.Vec2d(window_width / 2, window_height / 2)
        player_body.max_velocity = self.run_speed

        super().__init__("assets/sprites/delver", delver_groups, player_body)

    def move(self, dt: float, move_angle: float):
        """Make the player move."""
        print(move_angle)
        self.run_animation("run")
        self.set_target_angle(-move_angle - 90)
        self.update_angle_to_target(dt)

        run_vector = angle_to_vector(move_angle)
        run_velocity: list[float] = [
            run_vector[0] * self.run_speed,
            run_vector[1] * self.run_speed,
        ]

        magnitude = math.sqrt(run_velocity[0] ** 2 + run_velocity[1] ** 2)
        if magnitude > self.run_speed:
            run_velocity[0] *= self.run_speed / magnitude
            run_velocity[1] *= self.run_speed / magnitude

        force = Vec2d(
            self.body.mass * run_velocity[0] / dt,
            self.body.mass * run_velocity[1] / dt,
        )
        self.body.apply_force_at_local_point(force)

    def stand(self):
        """ "Make the player stand."""
        self.run_animation(None)
        self.body.velocity = Vec2d(0, 0)

    def update(self, dt):
        super().update(dt)
