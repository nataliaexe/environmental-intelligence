from fastapi import APIRouter

from app.api.schemas.simulation import ScenarioRequest
from app.services.simulation import simulation_service


router = APIRouter(
    prefix="/simulation",
    tags=["simulation"],
)


@router.get("/status")
async def simulation_status() -> dict:
    return simulation_service.status()


@router.post("/start")
async def start_simulation(request: ScenarioRequest) -> dict:
    return simulation_service.start(request.scenario)


@router.post("/stop")
async def stop_simulation() -> dict:
    return simulation_service.stop()
