from ..tile import Tile
from .autotile_rule import AutotileRule, get_rule_group
from itertools import chain
import warnings
import json

# 0: no tile from the same layer
# 1: autotile tile
# 2: any tile within the same layer (including no tile)
# 3: tiles within the same layer with the same object type

with open("tileset_manager/tile/autotile/default_autotile_forms.json", "r") as file:
    autotile_forms = json.load(file)

default_rules = list(
    chain.from_iterable(
        [
            get_rule_group(autotile_forms["outer_corner"], (1, 0)),
            get_rule_group(autotile_forms["inner_corner"], (3, 0)),
            get_rule_group(autotile_forms["thin_t_junction"], (5, 0)),
            get_rule_group(autotile_forms["t_junction"], (7, 0)),
            get_rule_group(autotile_forms["straight"], (1, 2)),
            get_rule_group(autotile_forms["edge"], (3, 2)),
            get_rule_group(autotile_forms["thin_corner"], (5, 2)),
            get_rule_group(autotile_forms["d_junction"], (7, 2)),
            get_rule_group(autotile_forms["b_junction"], (9, 2)),
            get_rule_group(autotile_forms["fish_junction"], (9, 0)),
            get_rule_group(autotile_forms["straight_thin"], (11, 2), amount=2),
            get_rule_group(autotile_forms["diagonal_junction"], (11, 0), amount=2),
        ]
    )
) + [
    AutotileRule(autotile_forms["lone"], (0, 1)),
    AutotileRule(autotile_forms["cross"], (0, 2)),
    AutotileRule(autotile_forms["center"], (0, 3)),
]


class AutotileTile(Tile):
    is_center = False
    is_deep = True

    rules: list[AutotileRule]

    def __init__(
        self,
        position: tuple[int, int],
        object_type: str | None = None,
        rules=None,
    ):
        super().__init__(position, object_type)

        if rules is None:
            self.rules = default_rules

        self.display = None

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
        def find_display(rule_index: int):
            if rule_index >= len(self.rules):
                warnings.warn("No display found", UserWarning)
                return
            rule = self.rules[rule_index]

            for y, row in enumerate(rule.rule_matrix):
                for x, cell in enumerate(row):
                    if cell == 1:
                        continue
                    if cell == 2:
                        continue

                    neighbor_cell = filtered_neighbors[y, x]
                    if (neighbor_cell and cell == 0) or (
                        (not neighbor_cell) and cell == 3
                    ):
                        return find_display(rule_index + 1)

            return rule.display

        self.display = find_display(0)
