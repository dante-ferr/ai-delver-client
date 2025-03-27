class WorldObject:
    def __init__(self):
        self._position = (0.0, 0.0)

    @property
    def position(self):
        """Get the position of the world object."""
        return self._position

    @position.setter
    def position(self, position: tuple[float, float]):
        """Set the position of the world object."""
        self._position = position

    def update(self, dt):
        """Update the world object."""
        pass
