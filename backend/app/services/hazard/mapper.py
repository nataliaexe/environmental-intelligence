from app.domain.hazard import HazardDefinition
from app.domain.mission import Mission


def create_investigation_mission(
    hazard: HazardDefinition,
    region_id: str,
    priority: float,
) -> Mission:
    return Mission(
        id=f"MISSION-{hazard.id.upper()}",
        objective=f"investigate_{hazard.id}",
        region_id=region_id,
        priority=priority,
        required_capabilities=[
            capability.value
            for capability in hazard.compatible_capabilities
        ],
    )
