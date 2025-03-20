import pickle
from .level_factory.level_factory import LevelFactory
from typing import TYPE_CHECKING
from .level_selector import LevelSelector
from .level_toggler import LevelToggler
import json

if TYPE_CHECKING:
    from .grid_map.world_objects_map import WorldObjectsMap
    from .grid_map.editor_tilemap import EditorTilemap
    from src.editor.level.canvas_object import CanvasObject
    from .grid_map import MixedMap

with open("src/config.json", "r") as general_config_data:
    general_config = json.load(general_config_data)

LAYER_ORDER = general_config["layer_order"]

LEVEL_FILENAME = "data/level_saves/level_map.pkl"


class Level:
    def __init__(
        self,
        map: "MixedMap",
    ):
        self.map = map

        self.selector = LevelSelector()
        self.toggler = LevelToggler()

    def save(self):
        with open(LEVEL_FILENAME, "wb") as file:
            pickle.dump(self.map, file)


level = LevelFactory().level
