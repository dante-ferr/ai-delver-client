from pytiling import TilemapLayer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from editor.level.canvas_object import CanvasObject


class EditorTilemapLayer(TilemapLayer):
    def __init__(self, name: str, tileset, icon_path: str):
        super().__init__(name, tileset)
        self.icon_path = icon_path

        self.canvas_objects: list["CanvasObject"] = []

    def add_canvas_object(self, canvas_object: "CanvasObject"):
        self.canvas_objects.append(canvas_object)
