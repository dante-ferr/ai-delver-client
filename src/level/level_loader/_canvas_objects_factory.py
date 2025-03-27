from typing import TYPE_CHECKING, Callable
from ..canvas_object import CanvasObject

if TYPE_CHECKING:
    from ..level import Level


class CanvasObjectsFactory:
    def __init__(self, level: "Level"):
        self.level = level
        self.tilemap = level.map.tilemap
        self.world_objects_map = level.map.world_objects_map

    def create_canvas_objects(self):
        floor_layer = self.tilemap.get_layer("floor")
        floor_layer.canvas_object_manager.add_canvas_object(
            self._create_canvas_object(
                "floor",
                create_element_callback=lambda position: self.tilemap.create_basic_floor_at(
                    position, apply_formatting=True
                ),
                remove_element_callback=lambda position: floor_layer.remove_tile_at(
                    position, apply_formatting=True
                ),
            )
        )

        walls_layer = self.tilemap.get_layer("walls")
        walls_layer.canvas_object_manager.add_canvas_object(
            self._create_canvas_object(
                "wall",
                lambda position: self.tilemap.create_basic_wall_at(
                    position, apply_formatting=True
                ),
                remove_element_callback=lambda position: walls_layer.remove_tile_at(
                    position, apply_formatting=True
                ),
            )
        )

        self._add_entity_canvas_object_to_layer("delver", "essentials", unique=True)

        self._add_canvas_object_variations_to_layer(
            "goal",
            "essentials",
            ["battery_snack", "oil_drink", "uranium_cake"],
            unique=True,
        )

    def _add_canvas_object_variations_to_layer(
        self, canvas_object_name: str, layer_name: str, variations: list[str], **args
    ):
        layer = self.world_objects_map.get_layer(layer_name)

        for variation in variations:

            def _callback(position: tuple[int, int], variation=variation):
                nonlocal layer

                for element in layer.get_elements(
                    *[v for v in variations if v != variation]
                ):
                    layer.remove_element(element)

                world_object = layer.create_world_object_at(
                    position,
                    canvas_object_name,
                    tags=[f"variation_{variation}"],
                    **args,
                )

                return world_object

            layer.canvas_object_manager.add_canvas_object(
                self._create_canvas_object(
                    variation,
                    _callback,
                    path=f"assets/img/representations/{canvas_object_name}/{variation}.png",
                )
            )

    def _add_entity_canvas_object_to_layer(
        self, object_name: str, layer_name: str, **args
    ):
        layer = self.world_objects_map.get_layer(layer_name)
        layer.canvas_object_manager.add_canvas_object(
            self._create_canvas_object(
                object_name,
                lambda position: layer.create_world_object_at(
                    position, object_name, **args
                ),
            )
        )

    def _create_canvas_object(
        self,
        canvas_object_name: str,
        create_element_callback: Callable,
        remove_element_callback: Callable | None = None,
        path: str | None = None,
    ):
        if path is None:
            path = "assets/img/representations/" + canvas_object_name + ".png"
        return CanvasObject(
            canvas_object_name,
            path,
            create_element_callback=create_element_callback,
            remove_element_callback=remove_element_callback,
        )
