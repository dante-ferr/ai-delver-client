from typing import Any, cast, TYPE_CHECKING

if TYPE_CHECKING:
    from runtime.simulation import Simulation
    from runtime.simulation import DelverAction

DELVER_ANGLE_VAR = 5


def delver_action_controller(
    action: "DelverAction", simulation: "Simulation", dt: float
):
    simulation.add_delver_action(action)

    if action["move"]:
        simulation.delver.move(dt, action["move_angle"])
