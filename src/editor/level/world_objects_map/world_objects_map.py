from pytiling import GridMap
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from .world_objects_layer import WorldObjectsLayer


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
