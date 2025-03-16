import pickle
import os
import json
from pytiling import Tileset, AutotileTile, Tile
from .editor_tilemap.editor_tilemap_layer import EditorTilemapLayer
from .world_objects_map import WorldObjectsMap, WorldObjectsLayer
from typing import TYPE_CHECKING
from editor.level.canvas_object import CanvasObject
from .editor_tilemap import EditorTilemap

if TYPE_CHECKING:
    from .level import Level

with open(("editor/config.json"), "r") as file:
    editor_config_data = json.load(file)
LEVEL_FILENAME = "editor/level_editor/saves/levels/level.pkl"
MAP_SIZE = (
    editor_config_data["start_map_width"],
    editor_config_data["start_map_height"],
)
TILE_SIZE = (editor_config_data["tile_width"], editor_config_data["tile_height"])
MIN_GRID_SIZE = tuple(editor_config_data["min_grid_size"])
MAX_GRID_SIZE = tuple(editor_config_data["max_grid_size"])

with open("config.json", "r") as file:
    general_config_data = json.load(file)
layer_order: list[str] = general_config_data["layer_order"]
tilemap_layer_names: list[str] = general_config_data["tilemap_layer_names"]


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

        self.tilemap = self._create_tilemap()
        world_objects_map = self._create_entity_map()
        self._level = Level(self.tilemap, world_objects_map)

        self._create_canvas_objects(self.tilemap, world_objects_map)

    def _create_tilemap(self):
        layers = {
            "floor": EditorTilemapLayer(
                "floor",
                Tileset("assets/img/tilesets/dungeon/floor.png"),
                "assets/svg/floor.svg",
            ),
            "walls": EditorTilemapLayer(
                "walls",
                Tileset("assets/img/tilesets/dungeon/walls.png"),
                "assets/svg/walls.svg",
            ),
        }

        tilemap = EditorTilemap(TILE_SIZE, MAP_SIZE, MIN_GRID_SIZE, MAX_GRID_SIZE)
        for layer_name in layer_order:
            if layer_name in tilemap_layer_names:
                tilemap.add_layer(layers[layer_name])

        tilemap.add_layer_concurrence(layers["walls"], layers["floor"])

        self._create_starting_tiles(tilemap)
        return tilemap

    def _create_starting_tiles(self, tilemap: EditorTilemap):
        walls = tilemap.get_layer("walls")
        floor = tilemap.get_layer("floor")

        center = (MAP_SIZE[0] // 2, MAP_SIZE[1] // 2)

        floor.for_grid_position(
            lambda x, y: floor.add_tile(
                Tile(position=(x, y), display=(0, 0)), apply_formatting=False
            )
        )

        for x, y in tilemap.get_edge_positions():
            tile = AutotileTile(position=(x, y), autotile_object="wall")
            walls.add_tile(tile, apply_formatting=False)

        walls.formatter.format_all_tiles()

        starting_floor_tile = Tile(position=center, display=(0, 0))
        floor.add_tile(starting_floor_tile, apply_formatting=True)

        # for tile in walls.get_edge_tiles():
        #     tile.locked = True

    def _create_entity_map(self):
        essentials = WorldObjectsLayer("essentials", "assets/svg/important.svg")

        game_objects_map = WorldObjectsMap(
            TILE_SIZE, MAP_SIZE, MIN_GRID_SIZE, MAX_GRID_SIZE
        )
        game_objects_map.add_layer(essentials)

        return game_objects_map

    def _create_canvas_objects(
        self, tilemap: "EditorTilemap", world_objects_map: "WorldObjectsMap"
    ):
        floor = tilemap.get_layer("floor")
        floor.add_canvas_object(self._create_canvas_object("floor"))

        walls = tilemap.get_layer("walls")
        walls.add_canvas_object(self._create_canvas_object("wall"))

        essentials = world_objects_map.get_layer("essentials")
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
