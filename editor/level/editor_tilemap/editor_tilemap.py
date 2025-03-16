from pytiling import Tilemap
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from .editor_tilemap_layer import EditorTilemapLayer


class EditorTilemap(Tilemap):
    def __init__(
        self,
        tile_size: tuple[int, int],
        grid_size: tuple[int, int] = (5, 5),
        min_grid_size: tuple[int, int] = (5, 5),
        max_grid_size: tuple[int, int] = (100, 100),
    ):
        super().__init__(tile_size, grid_size, min_grid_size, max_grid_size)

    def get_layer(self, name: str) -> "EditorTilemapLayer":
        """Get a layer by its name."""
        return cast("EditorTilemapLayer", super().get_layer(name))
