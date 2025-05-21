from fastapi import APIRouter
from typing import Any

router = APIRouter(prefix="/example", tags=["Example"])


@router.post("/simulation_history")
async def read_item(simulation_history: Any):
    return
