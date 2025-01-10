from .slot import Slot
from typing import TypedDict, List, Optional
import pyglet
from typing import TYPE_CHECKING
import math

if TYPE_CHECKING:
    from .skeleton import Skeleton

def rotate_position(position, angle):
    x, y = position
    rad_angle = math.radians(-angle)
    return (
        x * math.cos(rad_angle) - y * math.sin(rad_angle),
        x * math.sin(rad_angle) + y * math.cos(rad_angle)
    )

class Bone:
    slots: dict[str, Slot]

    base_position: tuple[float, float]
    base_angle = 0.
    base_scale: tuple[float, float]

    position: tuple[float, float]
    angle = 0.
    scale: tuple[float, float]

    relative_position: tuple[float, float]
    relative_angle = 0.
    relative_scale: tuple[float, float]

    group: pyglet.graphics.Group

    skeleton = None

    def __init__(self, bone_info, group: pyglet.graphics.Group, skeleton: "Skeleton"):
        self.name = bone_info['name']
        self.group = group
        # self.parent = bone_info['parent']
        self.skeleton = skeleton

        self.base_position = (
            bone_info['transform']['x'] if 'transform' in bone_info and 'x' in bone_info['transform'] else 0.,
            bone_info['transform']['y'] if 'transform' in bone_info and 'y' in bone_info['transform'] else 0.
        )
        self.base_scale = (
            bone_info['transform']['scX'] if 'transform' in bone_info and 'scX' in bone_info['transform'] else 1.,
            bone_info['transform']['scY'] if 'transform' in bone_info and 'scY' in bone_info['transform'] else 1.
        )

        self.position = (0, 0)
        self.angle = (0)
        self.scale = (1, 1)

        self.set_position(0, 0, False)
        self.set_angle(0, False)
        self.set_scale(1, 1, False)

        self.slots = {}

    # def set_parent(self):
    #     if self.parent:
    #         self.parent = self.skeleton.bones[self.parent]
    
    def set_position(self, x: float, y: float, update=True):
        """Change bone's relative position. If update is True, the bone's actual position will be updated."""
        self.relative_position = (x + self.base_position[0], y + self.base_position[1])
        if update: self.update_position()
    
    def set_angle(self, angle: float, update=True):
        """Change bone's relative angle. If update is True, the bone's actual angle will be updated."""
        self.relative_angle = angle
        if update: self.update_angle()
    
    def set_scale(self, x: float, y: float, update=True):
        """Change bone's relative scale. If update is True, the bone's actual scale will be updated."""
        self.relative_scale = (x * self.base_scale[0], y * self.base_scale[0])
        if update:
            self.update_scale()

    def update_position(self):
        scaled_relative_position = (
            self.relative_position[0] * self.scale[0],
            self.relative_position[1] * self.scale[1]
        )
        rotated_position = rotate_position(scaled_relative_position, self.angle)
        self.position = (
            self.skeleton.position[0] + rotated_position[0],
            self.skeleton.position[1] + rotated_position[1]
        )
        # print(self.scale)
        # print(((self.relative_position[0]) * self.scale[0], (self.relative_position[1]) * self.scale[1]))

        for slot in self.slots.values():
            slot.update_position()
    
    def update_angle(self):
        self.angle = self.skeleton.angle + self.relative_angle

        self.update_position()
        for slot in self.slots.values():
            slot.update_angle()
    
    def update_scale(self):
        self.scale = (self.skeleton.scale[0] * self.relative_scale[0], self.skeleton.scale[1] * self.relative_scale[1])

        self.update_position()
        for slot in self.slots.values():
            slot.update_scale()