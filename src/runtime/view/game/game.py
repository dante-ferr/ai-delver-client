from .. import ViewableRuntime
from .game_controls import GameControls


class Game(ViewableRuntime):
    def _create_controls(self):
        self.controls = GameControls(self.keys)
        self.controls.append_delver(self.delver)
