from pytiling import GridMap
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from .world_objects_layer import WorldObjectsLayer
    from editor.level.canvas_object import CanvasObject
    from .world_object import WorldObjectRepresentation


class WorldObjectsMap(GridMap):
    def __init__(
        self,
        tile_size: tuple[int, int],
        size: tuple[int, int] = (5, 5),
        min_grid_size: tuple[int, int] = (5, 5),
        max_grid_size: tuple[int, int] = (100, 100),
    ):
        super().__init__(tile_size, size, min_grid_size, max_grid_size)

    def get_layer(self, name: str):
        """Get a layer by its name."""
        return cast("WorldObjectsLayer", super().get_layer(name))

    @property
    def canvas_objects(self):
        canvas_objects: dict[str, "CanvasObject"] = {}

        for layer in self.layers:
            layer = cast("WorldObjectsLayer", layer)
            for canvas_object in layer.canvas_object_manager.canvas_objects.values():
                canvas_objects[canvas_object.name] = canvas_object

        return canvas_objects

    @property
    def all_world_objects(self):
        return cast(list["WorldObjectRepresentation"], self.all_elements)
