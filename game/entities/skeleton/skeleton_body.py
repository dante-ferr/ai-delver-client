import pymunk
from typing import Literal


class SkeletonBody:
    def __init__(
        self,
        space: pymunk.Space,
        position: tuple[float, float] = (0, 0),
        mass: float = 1.0,
        radius: float = 10.0,
        elasticity: float = 0.8,
        friction: float = 0.5,
        damping: float = 1,
    ):
        """
        A Body object that holds the physics representation of the skeleton.

        Parameters:
        - skeleton: The Skeleton object that this body will be associated with.
        - mass: The mass of the body for physics simulation.
        - radius: The radius for the collision shape (for simplicity, assuming a circular shape).
        - position: The initial position of the body.
        """
        self.space = space

        self.body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = elasticity
        self.shape.friction = friction
        self.space.add(self.body, self.shape)

        self.body.position = pymunk.Vec2d(*position)
        self.normal_damping = damping
        self.damping = damping

        # self.circle = shapes.Circle(
        #     self.body.position.x,
        #     self.body.position.y,
        #     radius,
        #     color=(50, 50, 255),
        # )

    def update(self, dt):
        """Update the body position and the skeleton."""
        self.space.step(dt)

        vx, vy = self.body.velocity

        damping_factor = self.damping**dt
        new_vx = vx * damping_factor
        new_vy = vy * damping_factor

        self.body.velocity = new_vx, new_vy

        # self.circle.x = self.body.position.x
        # self.circle.y = self.body.position.y
        # self.circle.draw()

    def set_damping(self, damping: float | Literal["normal"] = "normal"):
        """Set the damping of the body. If damping is "normal", the normal damping will be used."""
        if damping == "normal":
            damping = self.normal_damping
        self.damping = damping

    def apply_force(self, force: pymunk.Vec2d):
        """Apply a force to the body."""
        self.body.apply_force_at_local_point(force)

    def set_velocity(self, velocity: pymunk.Vec2d):
        """Set the velocity of the body."""
        self.body.velocity = velocity
