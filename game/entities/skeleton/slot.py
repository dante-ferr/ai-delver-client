import pyglet
from .get_subtextures import Subtexture
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bone import Bone


class Slot:
    current_display: int

    bone = None
    name: str
    group = None

    relative_position: tuple[float, float]
    relative_angle = 0.0
    relative_scale: tuple[float, float]

    def __init__(
        self,
        slot_info,
        bone: "Bone",
        subtextures: list[Subtexture],
        batch: pyglet.graphics.Batch,
    ):
        self.name = slot_info["name"]
        self.subtextures = subtextures
        self.group = bone.group

        self.relative_position = (0, 0)
        self.relative_angle = 0
        self.relative_scale = (1, 1)

        default_display = slot_info.get("displayIndex", 1) - 1
        self.current_display = default_display
        default_subtexture = self.subtextures[default_display]["image"]

        self.sprite = pyglet.sprite.Sprite(
            default_subtexture, group=self.group, batch=batch
        )

    def change_display(self, display_index: int):
        """Change the sprite's texture."""
        self.current_display = display_index
        self.sprite.image = self.subtextures[display_index]["image"]

    def update_position(self):
        """Follow parent bone's position"""
        self.sprite.x = self.bone.position[0] + self.relative_position[0]
        self.sprite.y = self.bone.position[1] + self.relative_position[1]

    def update_angle(self):
        """Follow parent bone's angle"""
        self.sprite.rotation = self.bone.angle + self.relative_angle

    def update_scale(self):
        """Follow parent bone's scale"""
        self.sprite.scale_x = self.bone.scale[0] * self.relative_scale[0]
        self.sprite.scale_y = self.bone.scale[1] * self.relative_scale[1]
