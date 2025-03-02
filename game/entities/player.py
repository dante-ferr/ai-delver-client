import pyglet
from pyglet_dragonbones.skeleton import Skeleton
from pyglet_dragonbones.skeleton_body import SkeletonBody
import json
import pymunk

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

    def animation_run(self, animation_name: str | None, starting_frame=0, speed=1):
        self.animation.run(animation_name, starting_frame, speed)
