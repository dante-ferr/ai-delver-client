import pickle
import os
import json
from pytiling import Tilemap, Tileset, TilemapLayer, AutotileTile
from .entity_map import EntityMap, EntityLayer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .level import Level

with open(("editor/config.json"), "r") as file:
    config_data = json.load(file)

LEVEL_FILENAME = "editor/level_editor/saves/levels/level.pkl"


class LevelFactory:
    def __init__(self):
        self._level: "Level | None" = None
        self._load_level()

    def _load_level(self):
        if os.path.exists(LEVEL_FILENAME):
            try:
                with open(LEVEL_FILENAME, "rb") as file:
                    self._level = pickle.load(file)
                print("Loaded existing instance.")
            except Exception as e:
                print(f"Error loading instance: {e}. Creating a new one.")
                self._create_level()
        else:
            print("File not found. Creating a new instance.")
            self._create_level()

    def _create_level(self):
        self._create_tilemap()

    def _create_tilemap(self):
        from .level import Level

        walls = TilemapLayer(
            "walls", Tileset("assets/tilesets/dungeon/walls.png", (32, 32))
        )

        floor = TilemapLayer(
            "floor", Tileset("assets/tilesets/dungeon/floor.png", (32, 32))
        )

        tilemap = Tilemap(
            (config_data["start_tilemap_width"], config_data["start_tilemap_height"])
        )
        tilemap.add_layer(floor)
        tilemap.add_layer(walls)
        tilemap.add_layer_concurrence(walls, floor)

        def create_starting_tile(x, y):
            tile = AutotileTile(position=(x, y), autotile_object="wall")
            walls.add_tile(tile, apply_formatting=False)

        walls.for_grid_position(create_starting_tile)

        for tile in walls.get_edge_tiles():
            tile.locked = True

        player = EntityLayer("player")
        entity_map = EntityMap()
        entity_map.add_layer(player)

        self._level = Level(tilemap, entity_map)

    @property
    def level(self) -> "Level":
        if not self._level:
            raise ValueError("Level not loaded.")
        return self._level

    def _save_level(self):
        with open(LEVEL_FILENAME, "wb") as file:
            pickle.dump(self._level, file)
