from ..world_object import WorldObject
from typing import Optional
from pyglet import sprite, image
from pyglet.image.animation import Animation
from pyglet.graphics import Batch
from level import level_loader


class Item(WorldObject):
    def __init__(
        self,
        sprite_path: Optional[str] = None,
        animation: Optional[Animation] = None,
        batch: Optional[Batch] = None,
        size: tuple[int, int] = (24, 24),
    ):
        super().__init__()

        self.batch = batch
        self.size: tuple[int, int] = size
        self.sprite = self._create_sprite(sprite_path, animation)

        self.compensated = False

        self._update_sprite_position()

    def _create_sprite(
        self, sprite_path: Optional[str], animation: Optional[Animation]
    ):
        if sprite_path:
            img = image.load(sprite_path)
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2

            return sprite.Sprite(img, batch=self.batch)
        elif animation:
            for frame in animation.frames:
                frame.image.anchor_x = frame.image.width // 2
                frame.image.anchor_y = frame.image.height // 2

            return sprite.Sprite(animation, batch=self.batch)

    def _compensate_offset_centering(self):
        self.position = (
            self.position[0] + self.tile_size[0] / 2,
            self.position[1] + self.tile_size[1] / 2,
        )

    @property
    def position(self):
        return super().position

    @position.setter
    def position(self, position: tuple[float, float]):
        self._position = position
        if not self.compensated:
            self.compensated = True
            self._compensate_offset_centering()
        elif self.sprite:
            self._update_sprite_position()

    def _update_sprite_position(self):
        if self.sprite:
            self.sprite.update(x=self._position[0], y=self._position[1])

    def update(self, dt):
        """Update the item and its sprite if needed."""
        x, y = self.position
        width, height = self.size
        self.bounding_box = (
            x - width // 2,
            y - height // 2,
            x + width // 2,
            y + height // 2,
        )

    def draw(self, dt):
        """Draw the sprite if it exists."""
        if self.sprite:
            self.sprite.draw()

    def delete(self):
        """Clean up the sprite when no longer needed."""
        if self.sprite:
            self.sprite.delete()
