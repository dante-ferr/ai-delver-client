from pytiling import TilemapLayer
from editor.level.canvas_object import CanvasObjectsManager
import os

FLOOR_VARIATIONS_FILENAME = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "floor_variations.json"
)


class EditorTilemapLayer(TilemapLayer):
    def __init__(self, name: str, tileset, icon_path: str):
        super().__init__(name, tileset)
        self.icon_path = icon_path
        self.canvas_object_manager = CanvasObjectsManager()

    def create_basic_wall_at(self, position: tuple[int, int], **args):
        tile = self.create_autotile_tile_at(
            position,
            "wall",
            default_shallow_tile_variations=True,
            **args,
        )
        return tile

    def create_basic_floor_at(
        self, position: tuple[int, int], apply_formatting=False, **args
    ):
        tile = self.create_tile_at(position, (0, 0), "floor", **args)
        if tile is not None:
            tile.add_variations_from_json(
                FLOOR_VARIATIONS_FILENAME, apply_formatting=apply_formatting
            )

        return tile
