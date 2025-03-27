from ..world_objects.entities import WorldObjectsController
from ..world_objects import WorldObject
from level import level_loader
from ..world_objects.entities.delver import Delver
from typing import TYPE_CHECKING
from ..world_objects.items import Goal
from level.grid_map.world_objects_map.world_object import WorldObjectRepresentation

if TYPE_CHECKING:
    import pymunk


def world_objects_controller_factory(space: "pymunk.Space"):
    world_objects_controller = WorldObjectsController()

    def _place_world_object(world_object: "WorldObject", **args):
        world_object.position = level_loader.level.map.grid_pos_to_actual_pos(
            element.position
        )
        world_objects_controller.add_world_object(world_object, **args)

    def _delver_factory(element):
        delver = Delver(space=space)
        delver.set_angle(180)

        _place_world_object(delver, unique_identifier="delver")

    def _goal_factory(element: "WorldObjectRepresentation"):
        goal = Goal(element.canvas_object_name)

        _place_world_object(goal, unique_identifier="goal")

    world_objects_factories = {"delver": _delver_factory, "goal": _goal_factory}

    for element in level_loader.level.map.world_objects_map.all_elements:
        world_objects_factories[element.name](element)

    return world_objects_controller
