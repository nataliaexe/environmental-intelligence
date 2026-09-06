from fastapi import APIRouter

from app.domain.agent import (
    AgentState,
    AgentEnergy,
    AgentLocalization,
    EnvironmentalAgent,
)
from app.domain.environment import Environment
from app.domain.region import Region
from app.domain.sensor import Sensor


router = APIRouter(
    prefix="/environment",
    tags=["environment"],
)


demo_environment = Environment(
    id="ENV-001",
    name="Demo Ecosystem",
    regions=[
        Region(
            id="REGION-001",
            name="North Sector",
            latitude=0.0,
            longitude=0.0,
        ),
        Region(
            id="REGION-002",
            name="South Sector",
            latitude=1.0,
            longitude=1.0,
        ),
    ],
    sensors=[
        Sensor(
            id="SENSOR-001",
            region_id="REGION-001",
            name="Environmental Node 01",
            sensor_type="multi",
            status="online",
        ),
        Sensor(
            id="SENSOR-002",
            region_id="REGION-002",
            name="Environmental Node 02",
            sensor_type="multi",
            status="online",
        ),
    ],
    agents=[
        EnvironmentalAgent(
            id="AGENT-001",
            name="Environmental Agent 01",
            state=AgentState.IDLE,
            capabilities=[
                "temperature",
                "humidity",
                "mobility",
            ],
            localization=AgentLocalization(
                x=0.0,
                y=0.0,
            ),
            energy=AgentEnergy(
                level=100.0,
                health=100.0,
            ),
            trust_score=1.0,
        )
    ],
)


@router.get("")
async def get_environment() -> dict:
    return {
        "id": demo_environment.id,
        "name": demo_environment.name,
        "regions": [
            {
                "id": region.id,
                "name": region.name,
                "latitude": region.latitude,
                "longitude": region.longitude,
                "health_score": region.health_score,
            }
            for region in demo_environment.regions
        ],
        "sensors": [
            {
                "id": sensor.id,
                "region_id": sensor.region_id,
                "name": sensor.name,
                "sensor_type": sensor.sensor_type,
                "status": sensor.status,
            }
            for sensor in demo_environment.sensors
        ],
        "agents": [
            {
                "id": agent.id,
                "name": agent.name,
                "state": agent.state.value,
                "capabilities": agent.capabilities,
                "position": {
                    "x": agent.localization.x,
                    "y": agent.localization.y,
                    "z": agent.localization.z,
                },
                "energy": agent.energy.level,
                "health": agent.energy.health,
                "trust_score": agent.trust_score,
                "current_mission_id": (
                    agent.current_mission_id
                ),
            }
            for agent in demo_environment.agents
        ],
    }
