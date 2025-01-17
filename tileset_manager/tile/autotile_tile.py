from .tile import Tile
from ..tilemap_layer import TilemapLayer


class AutotileTile(Tile):
    default_tile_positions = {
        "top": (2, 0),
        "bottom": (2, 2),
        "left": (1, 1),
        "right": (3, 1),
        # Fully surrounded by neighbors:
        "center": (2, 1),
        # Lone tile, with no neighbors:
        "lone": (8, 2),
        # Outer corners:
        "top_left": (1, 0),
        "top_right": (3, 0),
        "bottom_left": (1, 2),
        "bottom_right": (3, 2),
        # Inner corners:
        "inner_top_left": (4, 0),
        "inner_top_right": (5, 0),
        "inner_bottom_left": (4, 1),
        "inner_bottom_right": (5, 1),
        # T-juntions (three neighbors):
        "t_junction_top": (6, 0),
        "t_junction_bottom": (6, 1),
        "t_junction_left": (7, 1),
        "t_junction_right": (7, 0),
        # Fully connected to all sides:
        "cross": (3, 3),
        # Corners with two neighbors:
        "top_left_corner": (6, 2),
        "top_right_corner": (7, 2),
        "bottom_left_corner": (6, 3),
        "bottom_right_corner": (7, 3),
        # Edges (one neighbor):
        "top_edge": (4, 2),
        "bottom_edge": (4, 3),
        "left_edge": (5, 3),
        "right_edge": (5, 2),
        # Straight edges (two neighbors):
        "horizontal_edge": (2, 3),
        "vertical_edge": (1, 3),
        # Inner junctions (6 neighbors):
        "inner_t_junction_top": (8, 0),
        "inner_t_junction_bottom": (8, 1),
        "inner_t_junction_left": (9, 1),
        "inner_t_junction_right": (9, 0),
    }

    is_center = False
    is_deep = True

    def __init__(
        self,
        position: tuple[int, int],
        object_type: str | None = None,
        tile_positions=None,
    ):
        super().__init__(position, object_type)

        if tile_positions is None:
            self.tile_positions = self.default_tile_positions

        self.display = self.tile_positions["lone"]

    def format(self):
        if self.layer is None:
            return

        neighbors = self.layer.get_neighbors_of(self, same_object_type=True)
        self._position_format(neighbors)

        if self.is_center:
            range_2_neighbors_amount = self.layer.get_neighbors_of(
                self, radius=2, same_object_type=True, output_type="amount"
            )
            if range_2_neighbors_amount == 0:
                self.is_deep = True

        super().format()

    def _position_format(self, filtered_neighbors):
        top_left = filtered_neighbors[0, 0]
        top = filtered_neighbors[1, 0]
        top_right = filtered_neighbors[2, 0]
        left = filtered_neighbors[0, 1]
        right = filtered_neighbors[2, 1]
        bottom_left = filtered_neighbors[0, 2]
        bottom = filtered_neighbors[1, 2]
        bottom_right = filtered_neighbors[2, 2]

        if (
            top_left
            and top
            and top_right
            and left
            and right
            and bottom_left
            and bottom
            and bottom_right
        ):
            self.is_center = True
            self.display = self.tile_positions["center"]
        elif (
            top_left and top and top_right and left and right and bottom_left and bottom
        ):
            self.display = self.tile_positions["inner_top_left"]
        elif (
            top_left
            and top
            and top_right
            and left
            and right
            and bottom
            and bottom_right
        ):
            self.display = self.tile_positions["inner_top_right"]
        elif (
            top
            and top_right
            and right
            and bottom_right
            and bottom
            and bottom_left
            and left
        ):
            self.display = self.tile_positions["inner_bottom_right"]
        elif (
            top_left
            and top
            and left
            and bottom_left
            and bottom
            and bottom_right
            and right
        ):
            self.display = self.tile_positions["inner_bottom_left"]
        elif top_left and top and top_right and left and right and bottom:
            self.display = self.tile_positions["inner_t_junction_top"]
        elif top and top_right and left and right and bottom and bottom_right:
            self.display = self.tile_positions["inner_t_junction_right"]
        elif top and left and right and bottom_left and bottom and bottom_right:
            self.display = self.tile_positions["inner_t_junction_bottom"]
        elif top_left and top and left and right and bottom_left and bottom:
            self.display = self.tile_positions["inner_t_junction_left"]
        elif top and left and right and bottom:
            self.display = self.tile_positions["inner_cross"]
        elif right and bottom and bottom_right:
            self.display = self.tile_positions["top_left"]
        elif left and bottom_left and bottom:
            self.display = self.tile_positions["top_right"]
        elif top and top_right and right:
            self.display = self.tile_positions["bottom_left"]
        elif top_left and top and left:
            self.display = self.tile_positions["bottom_right"]
        elif left and right and bottom:
            self.display = self.tile_positions["t_junction_top"]
        elif top and left and bottom:
            self.display = self.tile_positions["t_junction_right"]
        elif top and left and right:
            self.display = self.tile_positions["t_junction_bottom"]
        elif top and right and bottom:
            self.display = self.tile_positions["t_junction_left"]
        elif top and bottom:
            self.display = self.tile_positions["vertical_edge"]
        elif left and right:
            self.display = self.tile_positions["horizontal_edge"]
        elif right and bottom:
            self.display = self.tile_positions["top_left_corner"]
        elif left and bottom:
            self.display = self.tile_positions["top_right_corner"]
        elif top and right:
            self.display = self.tile_positions["bottom_left_corner"]
        elif top and left:
            self.title = self.tile_positions["bottom_right_corner"]
        elif top:
            self.display = self.tile_positions["top_edge"]
        elif right:
            self.display = self.tile_positions["right_edge"]
        elif bottom:
            self.display = self.tile_positions["bottom_edge"]
        elif left:
            self.display = self.tile_positions["left_edge"]
        else:
            self.display = self.tile_positions["lone"]
