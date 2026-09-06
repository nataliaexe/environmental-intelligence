from dataclasses import dataclass

from app.domain.mission import Mission
from app.domain.swarm import SwarmObjective


@dataclass(frozen=True)
class PlannedMission:
    mission: Mission
    objective: SwarmObjective


class MissionPlanner:
    def plan(
        self,
        mission: Mission,
    ) -> PlannedMission:
        objective_type = self._resolve_objective(
            mission.objective
        )

        minimum_agents = self._minimum_agents(
            objective_type
        )

        target_coverage = self._target_coverage(
            objective_type
        )

        return PlannedMission(
            mission=mission,
            objective=SwarmObjective(
                type=objective_type,
                target_region_id=mission.region_id,
                priority=mission.priority,
                target_coverage=target_coverage,
                minimum_agents=minimum_agents,
                required_capabilities=list(
                    mission.required_capabilities
                ),
            ),
        )

    @staticmethod
    def _resolve_objective(
        objective: str,
    ) -> str:
        mapping = {
            "investigate_wildfire": "investigate",
            "investigate_flood": "investigate",
            "investigate_drought": "investigate",
            "increase_sensor_density": "increase_coverage",
            "increase_water_monitoring": "increase_coverage",
            "map_affected_region": "map_region",
            "communication_relay": "create_relay",
        }

        return mapping.get(
            objective,
            objective,
        )

    @staticmethod
    def _minimum_agents(
        objective: str,
    ) -> int:
        if objective == "investigate":
            return 3

        if objective == "increase_coverage":
            return 4

        if objective == "map_region":
            return 6

        if objective == "create_relay":
            return 3

        return 1

    @staticmethod
    def _target_coverage(
        objective: str,
    ) -> float:
        if objective == "investigate":
            return 0.7

        if objective == "increase_coverage":
            return 0.9

        if objective == "map_region":
            return 0.95

        if objective == "create_relay":
            return 0.8

        return 0.5


mission_planner = MissionPlanner()
