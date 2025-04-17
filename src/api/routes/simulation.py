from fastapi import APIRouter
from runtime.simulation import simulation_controller
from typing import cast
from fastapi.responses import JSONResponse
import json
from .delver_action_controller import delver_action_controller

with open("src/runtime/config.json", "r") as file:
    config = json.load(file)
DT = 1 / config["fps"] * 3

router = APIRouter()


@router.post("/step")
def step_simulation(action: dict[str, float]):
    simulation = simulation_controller.current_simulation
    delver_action_controller(action, simulation, DT)

    simulation.update(DT)

    reward = -1
    ended = False

    if simulation.delver.check_collision(simulation.goal):
        reward = 100
        ended = True

    return reward, ended, simulation.elapsed_time


@router.get("/walls")
def get_walls():
    import numpy as np

    walls_grid = simulation_controller.current_simulation.tilemap.get_layer(
        "walls"
    ).grid
    walls_grid_presence = np.array(
        [[1 if cell is not None else 0 for cell in row] for row in walls_grid],
        dtype=np.uint8,
    )

    return JSONResponse(content=walls_grid_presence.tolist())


@router.post("/start_new_simulation")
def start_new_simulation():
    simulation_controller.start_new_simulation()


@router.get("/delver_position")
def get_delver_position():
    return simulation_controller.current_simulation.delver.position


@router.get("/goal_position")
def get_goal_position():
    return simulation_controller.current_simulation.goal.position


@router.get("/delver_angle")
def get_delver_angle():
    return simulation_controller.current_simulation.delver.angle
