import pickle
import os
import json
from pytiling import Tileset, AutotileTile, Tile
from ..grid_map.editor_tilemap.editor_tilemap_layer import EditorTilemapLayer
from ..grid_map.world_objects_map import WorldObjectsMap, WorldObjectsLayer
from typing import TYPE_CHECKING, Callable
from editor.level.canvas_object import CanvasObject
from ..grid_map.editor_tilemap import EditorTilemap
from ..grid_map import MixedMap
from ._canvas_objects_factory import CanvasObjectsFactory

if TYPE_CHECKING:
    from ..level import Level

with open(("src/editor/config.json"), "r") as file:
    editor_config_data = json.load(file)

LEVEL_FILENAME = "editor/level_editor/saves/levels/level.pkl"
MAP_SIZE = (
    editor_config_data["start_map_width"],
    editor_config_data["start_map_height"],
)
TILE_SIZE = (editor_config_data["tile_width"], editor_config_data["tile_height"])
MIN_GRID_SIZE = tuple(editor_config_data["min_grid_size"])
MAX_GRID_SIZE = tuple(editor_config_data["max_grid_size"])

with open("src/config.json", "r") as file:
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
                    self.level = pickle.load(file)
                print("Loaded existing instance.")
            except Exception as e:
                print(f"Error loading instance: {e}. Creating a new one.")
                self._create_level()
        else:
            print("File not found. Creating a new instance.")
            self._create_level()

    def _create_level(self):
        from ..level import Level

        mixed_map = MixedMap(TILE_SIZE, MAP_SIZE, MIN_GRID_SIZE, MAX_GRID_SIZE)
        self.tilemap = mixed_map.tilemap
        self.world_objects_map = mixed_map.world_objects_map
        self._configure_tilemap()
        self._configure_world_objects_map()
        mixed_map.populate_layers()

        self.level = Level(mixed_map)
        self.level.map.add_layer_concurrence("walls", "essentials")

        CanvasObjectsFactory(self.level).create_canvas_objects()

    def _configure_tilemap(self):
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

        for layer_name in layer_order:
            if layer_name in tilemap_layer_names:
                self.tilemap.add_layer(layers[layer_name])

        self.tilemap.add_layer_concurrence("walls", "floor")

        self._create_starting_tiles()
        self.tilemap.lock_boundary_walls_if_needed()

    def _create_starting_tiles(self):
        for x in range(1, self.tilemap.grid_size[0] - 1):
            for y in range(1, self.tilemap.grid_size[1] - 1):
                self.tilemap.create_basic_floor_at((x, y), apply_formatting=False)

        for position in self.tilemap.get_edge_positions():
            self.tilemap.create_basic_wall_at(position, apply_formatting=False)

        self.tilemap.format_all_tiles()

    def _configure_world_objects_map(self):
        essentials = WorldObjectsLayer("essentials", "assets/svg/important.svg")
        self.world_objects_map.add_layer(essentials)

    @property
    def level(self) -> "Level":
        if not self._level:
            raise ValueError("Level not loaded.")
        return self._level

    @level.setter
    def level(self, level: "Level"):
        self._level = level
