from typing import TYPE_CHECKING
from .level_selector import LevelSelector
from .level_toggler import LevelToggler
import json
import dill

if TYPE_CHECKING:
    from .grid_map import MixedMap

with open("src/config.json", "r") as general_config_data:
    general_config = json.load(general_config_data)

LAYER_ORDER = general_config["layer_order"]

SAVE_FILENAME = "data/level_saves/level.pkl"


class Level:
    def __init__(
        self,
        map: "MixedMap",
    ):
        self.map = map

        self.selector = LevelSelector()
        self.toggler = LevelToggler()

        self._name = "My custom level"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def __getstate__(self):
        state = self.__dict__.copy()
        state["selector"] = None
        state["toggler"] = None

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

        self.selector = LevelSelector()
        self.toggler = LevelToggler()

    def save(self):
        with open(SAVE_FILENAME, "wb") as file:
            dill.dump(self, file)
