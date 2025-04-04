import pyglet
from pyglet_dragonbones.skeleton import Skeleton
from .delver_body import DelverBody
import json
import pymunk
from ..skeletal_entity import SkeletalEntity

delver_groups = {
    "head": pyglet.graphics.Group(3),
    "left_foot": pyglet.graphics.Group(0),
    "right_foot": pyglet.graphics.Group(0),
    "body": pyglet.graphics.Group(1),
    "left_hand": pyglet.graphics.Group(2),
    "right_hand": pyglet.graphics.Group(2),
}


class Delver(SkeletalEntity):
    move_speed = 200
    run_angle = 0.0

    def __init__(self, space: pymunk.Space):
        mass = 1
        radius = 10

        body = DelverBody(mass=mass, moment=pymunk.moment_for_circle(mass, 0, radius))
        self.body = body
        shape = pymunk.Circle(body, radius)
        shape.collision_type = 1
        space.add(body, shape)
        super().__init__(body)

        body.setup_collision_handlers()
        body.max_velocity = self.move_speed

        self.skeleton = Skeleton("assets/img/sprites/delver", delver_groups)

    def update(self, dt):
        self.skeleton.set_position(self.body.position.x, self.body.position.y)
        self.skeleton.update(dt)
        self.body.update(dt)

        super().update(dt)
