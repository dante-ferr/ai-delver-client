from fastapi import APIRouter
from runtime.simulation import simulation_controller
from typing import cast
import numpy as np

router = APIRouter()


@router.post("/step")
def step_simulation(action: dict[str, float]):
    simulation = simulation_controller.current_simulation
    simulation.add_delver_action(action)

    move_direction = cast(float, action["move_direction"])
    if move_direction != 360.0:
        simulation.delver.move(1, move_direction)

    simulation.update(1)

    reward = -1
    ended = False

    if simulation.delver.check_collision(simulation.goal):
        reward = 100
        ended = True

    return reward, ended, simulation.elapsed_time


@router.get("/walls")
def get_walls():
    return np.where(
        simulation_controller.current_simulation.tilemap.get_layer("walls").grid
        is not None,
        1,
        0,
    ).astype(np.int32)


@router.post("/start_new_simulation")
def start_new_simulation():
    simulation_controller.start_new_simulation()


@router.get("/delver_position")
def get_delver_position():
    return simulation_controller.current_simulation.delver.position


@router.get("/goal_position")
def get_goal_position():
    return simulation_controller.current_simulation.goal.position
