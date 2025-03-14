import pickle
import os
import json
from pytiling import Tilemap, Tileset, AutotileTile
from .tilemap.editor_tilemap_layer import EditorTilemapLayer
from .world_objects_map import WorldObjectsMap, WorldObjectsLayer
from typing import TYPE_CHECKING
from editor.level.canvas_object import CanvasObject

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

        tilemap = self._create_tilemap()
        entity_map = self._create_entity_map()
        self._level = Level(tilemap, entity_map)

        self._create_canvas_objects(tilemap, entity_map)

    def _create_tilemap(self):
        walls = EditorTilemapLayer(
            "walls",
            Tileset("assets/img/tilesets/dungeon/walls.png", TILE_SIZE),
            "assets/svg/walls.svg",
        )
        floor = EditorTilemapLayer(
            "floor",
            Tileset("assets/img/tilesets/dungeon/floor.png", TILE_SIZE),
            "assets/svg/floor.svg",
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
        essentials = WorldObjectsLayer(
            "essentials", TILE_SIZE, "assets/svg/important.svg"
        )

        game_objects_map = WorldObjectsMap(MAP_SIZE)
        game_objects_map.add_layer(essentials)

        return game_objects_map

    def _create_canvas_objects(self, tilemap: "Tilemap", entity_map: "WorldObjectsMap"):
        floor = tilemap.get_layer("floor")
        if floor:
            floor.add_canvas_object(self._create_canvas_object("floor"))

        walls = tilemap.get_layer("walls")
        if walls:
            walls.add_canvas_object(self._create_canvas_object("wall"))

        essentials = entity_map.get_layer("essentials")
        if essentials:
            essentials.add_canvas_object(self._create_canvas_object("delver"))

    def _create_canvas_object(self, canvas_object_name: str):
        path = "assets/img/representations/" + canvas_object_name + ".png"
        return CanvasObject(canvas_object_name, path)

    @property
    def level(self) -> "Level":
        if not self._level:
            raise ValueError("Level not loaded.")
        return self._level

    def _save_level(self):
        with open(LEVEL_FILENAME, "wb") as file:
            pickle.dump(self._level, file)
