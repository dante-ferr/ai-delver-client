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
    elif top_left and top and top_right and left and right and bottom_left and bottom:
        self.display = self.tile_positions["inner_top_left"]
    elif top_left and top and top_right and left and right and bottom and bottom_right:
        self.display = self.tile_positions["inner_top_right"]
    elif (
        top and top_right and right and bottom_right and bottom and bottom_left and left
    ):
        self.display = self.tile_positions["inner_bottom_right"]
    elif (
        top_left and top and left and bottom_left and bottom and bottom_right and right
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
    elif left and right and bottom_left and bottom and bottom_right:
        self.display = self.tile_positions["top"]
    elif top_left and top and top_right and left and right:
        self.display = self.tile_positions["bottom"]
    elif top and top_right and right and bottom and bottom_right:
        self.display = self.tile_positions["left"]
    elif top_left and top and left and bottom_left and bottom:
        self.display = self.tile_positions["right"]
    elif top and left and right and bottom:
        self.display = self.tile_positions["cross"]
    elif left and right and bottom and bottom_right:
        self.display = self.tile_positions["p_junction_top_left"]
    elif top and left and bottom_left and bottom:
        self.display = self.tile_positions["p_junction_top_right"]
    elif top and top_right and right and bottom:
        self.display = self.tile_positions["p_junction_bottom_left"]
    elif top_left and top and left and right:
        self.display = self.tile_positions["p_junction_bottom_right"]
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
