from typing import TypedDict, Literal, Any
from .tile.tile import Tile
import numpy as np
from .tileset import Tileset


class Area(TypedDict):
    top_left: tuple[int, int]
    bottom_right: tuple[int, int]


class TilemapLayer:
    def __init__(self, name: str, tileset: Tileset):
        self.name = name
        self.grid = np.empty((8, 8), dtype=Tile)
        self.tileset = tileset

    def add_tile(self, tile: Tile, apply_formatting=True):
        tile.set_layer(self)
        self.grid[*tile.position] = tile

        if apply_formatting:
            self.format(self._get_area_around(tile.position, 1))

    def set_size(self, size: tuple[int, int]):
        np.resize(self.grid, size)

    def format(self, area: Area | Literal["all"] = "all"):
        radius = 2
        if area == "all":
            area = Area(
                top_left=(0, 0),
                bottom_right=(self.grid.shape[0] - radius, self.grid.shape[1] - radius),
            )

        def tile_format_callback(x, y):
            tile = self.grid[x, y]
            if tile is not None:
                tile.format()

        self._loop_over_area(area, tile_format_callback)

    def get_neighbors_of(
        self,
        tile: Tile,
        radius: int = 1,
        same_object_type=False,
        output_type: Literal["tile_grid", "bool_grid", "amount"] = "bool_grid",
    ):
        """Get the neighbors of a tile in a given radius. If output_type is "grid", it returns a numpy array of tuples, where each tuple represents a neighbor's position. If output_type is "amount", it returns the amount of neighbors."""
        neighbors: Any

        if output_type == "tile_grid":
            neighbors = np.empty((3, 3), dtype=Tile)
        elif output_type == "bool_grid":
            neighbors = np.full((3, 3), False)
        elif output_type == "amount":
            neighbors = 0

        def tile_neighbors_callback(x, y):
            nonlocal neighbors

            if x == tile.position[0] and y == tile.position[1]:
                return
            neighbor = self.grid[x, y]
            if neighbor is None:
                return
            if same_object_type and neighbor.object_type != tile.object_type:
                return

            if output_type == "grid":
                neighbors[
                    x - tile.position[0] + radius, y - tile.position[1] + radius
                ] = neighbor
            elif output_type == "bool_grid":
                neighbors[
                    x - tile.position[0] + radius, y - tile.position[1] + radius
                ] = True
            elif output_type == "amount":
                neighbors += 1

        self._loop_over_area(
            self._get_area_around(tile.position, radius), tile_neighbors_callback
        )
        return neighbors

    def _loop_over_area(self, area: Area, callback):
        top_left_x, top_left_y = area["top_left"]
        bottom_right_x, bottom_right_y = area["bottom_right"]

        for x in range(top_left_x, bottom_right_x + 1):
            for y in range(top_left_y, bottom_right_y + 1):
                callback(x, y)

    def _get_area_around(self, center: tuple[int, int], radius: int) -> Area:
        center_x, center_y = center
        grid_width, grid_height = self.grid.shape

        top_left_x = max(center_x - radius, 0)
        top_left_y = max(center_y - radius, 0)
        bottom_right_x = min(center_x + radius, grid_width - 1)
        bottom_right_y = min(center_y + radius, grid_height - 1)

        return Area(
            top_left=(top_left_x, top_left_y),
            bottom_right=(bottom_right_x, bottom_right_y),
        )
