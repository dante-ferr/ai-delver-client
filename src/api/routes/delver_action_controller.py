from typing import Any, cast, TYPE_CHECKING

if TYPE_CHECKING:
    from runtime.simulation import Simulation

delver_angle_var = 5


def delver_action_controller(action: Any, simulation: "Simulation", dt: float):
    simulation.add_delver_action(action)

    move_command = action["move"]

    move_direction = simulation.delver.angle
    if move_command == 0:
        return
    elif move_command == 1:
        move_direction += delver_angle_var * -1
    elif move_command == 2:
        move_direction += delver_angle_var
    elif move_command == 3:
        pass  # Keep move direction unchanged

    simulation.delver.move(dt, move_direction)
