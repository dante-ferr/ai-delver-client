from pyglet import window
from typing import TYPE_CHECKING
from utils import vector_to_angle
from ..view_controls import ViewControls

if TYPE_CHECKING:
    from ...world_objects.entities.delver import Delver


class GameControls(ViewControls):
    keys: window.key.KeyStateHandler

    def __init__(self, keys: window.key.KeyStateHandler):
        super().__init__(keys)

    def _update_delver_controls(self, dt):
        run_vector = [0, 0]

        if self.keys[window.key.RIGHT]:
            run_vector[0] += 1
        if self.keys[window.key.LEFT]:
            run_vector[0] -= 1
        if self.keys[window.key.UP]:
            run_vector[1] += 1
        if self.keys[window.key.DOWN]:
            run_vector[1] -= 1

        if run_vector == [0, 0]:
            self.delver.stand()
        else:
            self.delver.move(dt, vector_to_angle(run_vector))

    def update(self, dt):
        self._update_delver_controls(dt)
