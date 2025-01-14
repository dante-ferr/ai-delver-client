import pymunk
from pyglet import shapes
from .skeleton import Skeleton  # Assuming the Skeleton class is defined elsewhere


class SkeletonBody:
    def __init__(
        self,
        skeleton: Skeleton,
        mass: float = 1.0,
        radius: float = 10.0,
        position: tuple[float, float] = (0, 0),
    ):
        """
        A Body object that holds the physics representation of the skeleton.

        Parameters:
        - skeleton: The Skeleton object that this body will be associated with.
        - mass: The mass of the body for physics simulation.
        - radius: The radius for the collision shape (for simplicity, assuming a circular shape).
        - position: The initial position of the body.
        """
        self.skeleton = skeleton
        self.position = pymunk.Vec2d(*position)

        self.space = pymunk.Space()
        self.body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
        self.body.position = self.position

        # Create a circular shape for collision (this can be expanded)
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 0.8  # Set some elasticity for bouncy effect
        self.shape.friction = 0.5  # Set the friction for collisions
        self.space.add(self.body, self.shape)

        # Optional: Create a pyglet circle to visually represent the body
        self.circle = shapes.Circle(
            self.body.position.x,
            self.body.position.y,
            radius,
            color=(50, 50, 255),
            batch=self.skeleton.batch,
        )

    def update(self, dt):
        """Update the body position and the skeleton."""
        # Update physics space
        self.space.step(dt)

        # Update the skeleton's position based on the physics body
        self.skeleton.set_position(self.body.position.x, self.body.position.y)

        # Update the visual representation (circle)
        self.circle.x = self.body.position.x
        self.circle.y = self.body.position.y

    def apply_force(self, force: pymunk.Vec2d):
        """Apply a force to the body."""
        self.body.apply_force_at_local_point(force)

    def set_velocity(self, velocity: tuple[float, float]):
        """Set the velocity of the body."""
        self.body.velocity = pymunk.Vec2d(*velocity)
