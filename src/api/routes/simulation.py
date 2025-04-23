from fastapi import WebSocket, APIRouter
from typing import Any, Literal, TypedDict, cast
import numpy as np
import json
from runtime.simulation import simulation_controller
from .delver_action_controller import delver_action_controller
from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from runtime.simulation import DelverAction

with open("src/runtime/config.json", "r") as file:
    config = json.load(file)

DT = 1 / config["fps"] * 3
router = APIRouter()


class Message(TypedDict):
    type: Literal[
        "step",
        "get_walls",
        "start_new_simulation",
        "get_delver_position",
        "get_goal_position",
        "get_delver_angle",
    ]
    payload: dict[str, Any]


class SimulationWebSocketHandler:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.simulation = simulation_controller.current_simulation

    async def handle(self):
        await self.websocket.accept()
        while True:
            try:
                data: Message = await self.websocket.receive_json()
                msg_type = data["type"]
                payload = data.get("payload", {})

                handler = getattr(self, f"handle_{msg_type}", self.handle_unknown)
                await handler(payload)
            except Exception as e:
                await self.websocket.send_json({"error": str(e)})

    async def handle_step(self, payload: dict[str, Any]):
        delver_action_controller(cast("DelverAction", payload), self.simulation, DT)
        self.simulation.update(DT)

        reward = (
            100 if self.simulation.delver.check_collision(self.simulation.goal) else -1
        )
        ended = reward == 100

        await self.websocket.send_json(
            {
                "type": "step_result",
                "reward": reward,
                "ended": ended,
                "elapsed_time": self.simulation.elapsed_time,
            }
        )

    async def handle_get_walls(self, _: dict[str, Any]):
        walls_grid = self.simulation.tilemap.get_layer("walls").grid
        walls_grid_presence = np.array(
            [[1 if cell is not None else 0 for cell in row] for row in walls_grid],
            dtype=np.uint8,
        )
        await self.websocket.send_json(
            {"type": "walls_data", "walls": walls_grid_presence.tolist()}
        )

    async def handle_start_new_simulation(self, _: dict[str, Any]):
        simulation_controller.start_new_simulation()
        self.simulation = simulation_controller.current_simulation
        await self.websocket.send_json({"type": "start_new_simulation_ack"})

    async def handle_get_delver_position(self, _: dict[str, Any]):
        await self.websocket.send_json(
            {
                "type": "delver_position",
                "position": self.simulation.delver.position,
            }
        )

    async def handle_get_goal_position(self, _: dict[str, Any]):
        await self.websocket.send_json(
            {
                "type": "goal_position",
                "position": self.simulation.goal.position,
            }
        )

    async def handle_get_delver_angle(self, _: dict[str, Any]):
        await self.websocket.send_json(
            {
                "type": "delver_angle",
                "angle": self.simulation.delver.angle,
            }
        )

    async def handle_unknown(self, _: dict[str, Any]):
        await self.websocket.send_json({"error": "Unknown message type"})


@router.websocket("")
async def simulation_socket(websocket: WebSocket):
    handler = SimulationWebSocketHandler(websocket)
    await handler.handle()
