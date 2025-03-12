import pickle
import os
import json
from pytiling import Tilemap, Tileset, TilemapLayer, AutotileTile
from .game_objects_map import GameObjectsMap, GameObjectsLayer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .level import Level

with open(("editor/config.json"), "r") as file:
    config_data = json.load(file)

LEVEL_FILENAME = "editor/level_editor/saves/levels/level.pkl"
MAP_SIZE = (config_data["start_tilemap_width"], config_data["start_tilemap_height"])
TILE_SIZE = (config_data["tile_width"], config_data["tile_height"])


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
        from .level import Level

        self._level = Level(self._create_tilemap(), self._create_entity_map())

    def _create_tilemap(self):
        walls = TilemapLayer(
            "walls", Tileset("assets/tilesets/dungeon/walls.png", TILE_SIZE)
        )
        floor = TilemapLayer(
            "floor", Tileset("assets/tilesets/dungeon/floor.png", TILE_SIZE)
        )

        tilemap = Tilemap(MAP_SIZE)
        tilemap.add_layer(floor)
        tilemap.add_layer(walls)
        tilemap.add_layer_concurrence(walls, floor)

        def create_starting_tile(x, y):
            tile = AutotileTile(position=(x, y), autotile_object="wall")
            walls.add_tile(tile, apply_formatting=False)

        walls.for_grid_position(create_starting_tile)

        for tile in walls.get_edge_tiles():
            tile.locked = True

        return tilemap

    def _create_entity_map(self):
        player = GameObjectsLayer("player", TILE_SIZE)

        game_objects_map = GameObjectsMap(MAP_SIZE)
        game_objects_map.add_layer(player)

        return game_objects_map

    @property
    def level(self) -> "Level":
        if not self._level:
            raise ValueError("Level not loaded.")
        return self._level

    def _save_level(self):
        with open(LEVEL_FILENAME, "wb") as file:
            pickle.dump(self._level, file)
