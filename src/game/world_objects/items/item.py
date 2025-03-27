from ..world_object import WorldObject
from pyglet import sprite, image


class Item(WorldObject):
    def __init__(self, sprite_path=None, animation=None, batch=None):
        super().__init__()

        self.sprite = None
        self.batch = batch

        if sprite_path:
            img = image.load(sprite_path)
            self.sprite = sprite.Sprite(img, batch=self.batch)
        elif animation:
            self.sprite = sprite.Sprite(animation, batch=self.batch)

        self._update_sprite_position()

    @property
    def position(self):
        return super().position

    @position.setter
    def position(self, position: tuple[float, float]):
        self._position = position
        if self.sprite:
            self._update_sprite_position()

    def _update_sprite_position(self):
        if self.sprite:
            self.sprite.update(x=self._position[0], y=self._position[1])

    def update(self, dt):
        """Update the item and its sprite if needed."""
        self.draw()

    def draw(self):
        """Draw the sprite if it exists."""
        if self.sprite:
            self.sprite.draw()

    def delete(self):
        """Clean up the sprite when no longer needed."""
        if self.sprite:
            self.sprite.delete()
