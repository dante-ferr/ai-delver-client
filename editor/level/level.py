from .level_factory import LevelFactory
from typing import TYPE_CHECKING
from .level_selector import LevelSelector
from .level_toggler import LevelToggler

if TYPE_CHECKING:
    from .entity_map import EntityMap
    from pytiling import Tilemap


class Level:
    def __init__(self, tilemap: "Tilemap", entity_map: "EntityMap"):
        self.tilemap = tilemap
        self.entity_map = entity_map

        self.selector = LevelSelector()
        self.toggler = LevelToggler()

    @property
    def grid_size(self):
        return self.tilemap.grid_size

    @grid_size.setter
    def grid_size(self, size: tuple[int, int]):
        self.tilemap.grid_size = size

        tile_width, tile_height = self.tilemap.tile_size
        self.entity_map.size = (size[0] * tile_width, size[1] * tile_height)


level = LevelFactory().level
