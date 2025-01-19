from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from ..tilemap_layer import TilemapLayer


class Tile:
    potential_displays_chance_sum = 0.0

    def __init__(
        self,
        position: tuple[int, int] | None = None,
        object_type: str | None = None,
        display: tuple[int, int] | None = None,
    ):
        self.position = position
        self.object_type = object_type
        self.display: tuple[int, int] | None = None

        self.potential_displays: dict[tuple[int, int], float] = {}
        self.set_display(display)

    def set_layer(self, layer: "TilemapLayer"):
        self.layer = layer

    def set_position(self, position: tuple[int, int] | None):
        self.position = position

    def format(self):
        if len(self.potential_displays) > 0:
            chosen_chance = random.random() * self.potential_displays_chance_sum

            chance_sum = 0
            for potential_display, chance in self.potential_displays.items():
                chance_sum += chance
                if chosen_chance < chance_sum:
                    self.set_display(potential_display)
                    break

    def add_potential_display(self, tile_coordinates: tuple[int, int], chance: float):
        """Add a potential display to the tile. The tile will randomly choose one of the potential displays based on the chances provided. Therefore the chance can be any number, but the other potential displays added to this tile must be taken into account."""
        self.potential_displays[tile_coordinates] = chance
        self.potential_displays_chance_sum += chance

    def set_display(self, display: tuple[int, int] | None):
        self.display = display

    # def get_image(self):
    #     return self.tilemap.tileset.get_tile_image(self.position)
