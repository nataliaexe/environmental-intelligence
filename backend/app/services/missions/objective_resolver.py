from app.domain.simulation_contract import (
    SimulationBehaviorProfile,
)
from app.domain.swarm import SwarmObjective


class ObjectiveResolver:

    def resolve_behavior(
        self,
        objective: SwarmObjective,
    ) -> SimulationBehaviorProfile:
        return SimulationBehaviorProfile(
            objective.type
        )


objective_resolver = ObjectiveResolver()
