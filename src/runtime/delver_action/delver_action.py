from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from runtime.world_objects.entities.delver import Delver


class DelverAction:
    def __init__(self, move_direction=360.0):
        self.move_direction = move_direction
