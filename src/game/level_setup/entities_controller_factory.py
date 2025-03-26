from ..entities import EntitiesController
from level import level_loader
from ..entities.delver import Delver
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pymunk


def entities_controller_factory(space: "pymunk.Space"):
    entities_controller = EntitiesController()

    for element in level_loader.level.map.world_objects_map.all_elements:
        if element.name == "delver":
            delver = Delver(space=space)
            delver.set_angle(180)
            delver.position = level_loader.level.map.grid_pos_to_actual_pos(
                element.position
            )

            entities_controller.add_entity(delver, unique_identifier="delver")

    return entities_controller
