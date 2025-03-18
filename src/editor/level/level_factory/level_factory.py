import pickle
import os
import json
from pytiling import Tileset, AutotileTile, Tile
from ..grid_map.editor_tilemap.editor_tilemap_layer import EditorTilemapLayer
from ..grid_map.world_objects_map import WorldObjectsMap, WorldObjectsLayer
from typing import TYPE_CHECKING, Callable
from editor.level.canvas_object import CanvasObject
from ..grid_map.editor_tilemap import EditorTilemap

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
                    self._level = pickle.load(file)
                print("Loaded existing instance.")
            except Exception as e:
                print(f"Error loading instance: {e}. Creating a new one.")
                self._create_level()
        else:
            print("File not found. Creating a new instance.")
            self._create_level()

    def _create_level(self):
        from ..level import Level

        self._create_tilemap()
        self.world_objects_map = self._create_entity_map()
        self._level = Level(self.tilemap, self.world_objects_map)

        self._create_canvas_objects()

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

        self.tilemap = EditorTilemap(TILE_SIZE, MAP_SIZE, MIN_GRID_SIZE, MAX_GRID_SIZE)
        for layer_name in layer_order:
            if layer_name in tilemap_layer_names:
                self.tilemap.add_layer(layers[layer_name])

        self.tilemap.add_layer_concurrence(layers["walls"], layers["floor"])

        self._create_starting_tiles()

    def _create_starting_tiles(self):

        walls = self.tilemap.get_layer("walls")
        floor = self.tilemap.get_layer("floor")

        def _create_floor_callback(position: tuple[int, int]):
            floor.create_basic_floor_at(position, apply_formatting=False)

        floor.for_grid_position(_create_floor_callback)

        for position in self.tilemap.get_edge_positions():
            walls.create_basic_wall_at(position, apply_formatting=False)

        floor.formatter.format_all_tiles()
        walls.formatter.format_all_tiles()

        # for tile in walls.get_edge_tiles():
        #     tile.locked = True

    def _create_entity_map(self):
        essentials = WorldObjectsLayer("essentials", "assets/svg/important.svg")

        game_objects_map = WorldObjectsMap(
            TILE_SIZE, MAP_SIZE, MIN_GRID_SIZE, MAX_GRID_SIZE
        )
        game_objects_map.add_layer(essentials)

        return game_objects_map

    def _create_canvas_objects(self):
        floor_layer = self.tilemap.get_layer("floor")
        floor_layer.canvas_object_manager.add_canvas_object(
            self._create_canvas_object(
                "floor",
                lambda position: floor_layer.create_basic_floor_at(
                    position, apply_formatting=True
                ),
            )
        )

        walls_layer = self.tilemap.get_layer("walls")
        walls_layer.canvas_object_manager.add_canvas_object(
            self._create_canvas_object(
                "wall",
                lambda position: walls_layer.create_basic_wall_at(
                    position, apply_formatting=True
                ),
            )
        )

        self._add_entity_canvas_object_to_layer("delver", "essentials", unique=True)

        self._add_canvas_object_variations_to_layer(
            "goal",
            "essentials",
            ["battery_snack", "oil_drink", "uranium_cake"],
            unique=True,
        )

    def _add_canvas_object_variations_to_layer(
        self, canvas_object_name: str, layer_name: str, variations: list[str], **args
    ):
        layer = self.world_objects_map.get_layer(layer_name)

        for variation in variations:

            def _callback(position: tuple[int, int], variation=variation):
                nonlocal layer
                for element in layer.get_elements(
                    *[v for v in variations if v != variation]
                ):
                    layer.remove_element(element)

                return layer.create_world_object_at(position, variation, **args)

            layer.canvas_object_manager.add_canvas_object(
                self._create_canvas_object(
                    variation,
                    _callback,
                    path=f"assets/img/representations/{canvas_object_name}/{variation}.png",
                )
            )

    def _add_entity_canvas_object_to_layer(
        self, object_name: str, layer_name: str, **args
    ):
        layer = self.world_objects_map.get_layer(layer_name)
        layer.canvas_object_manager.add_canvas_object(
            self._create_canvas_object(
                object_name,
                lambda position: layer.create_world_object_at(
                    position, object_name, **args
                ),
            )
        )

    def _create_canvas_object(
        self, canvas_object_name: str, click_callback: Callable, path: str | None = None
    ):
        if path is None:
            path = "assets/img/representations/" + canvas_object_name + ".png"
        return CanvasObject(canvas_object_name, path, click_callback)

    @property
    def level(self) -> "Level":
        if not self._level:
            raise ValueError("Level not loaded.")
        return self._level

    def _save_level(self):
        with open(LEVEL_FILENAME, "wb") as file:
            pickle.dump(self._level, file)
