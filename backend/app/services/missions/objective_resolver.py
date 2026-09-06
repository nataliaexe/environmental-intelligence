from simulator.swarm.behavior_profile import BehaviorProfile
from simulator.swarm.behaviors.profiles.defaults import get_profile

from app.domain.swarm import SwarmObjective


class ObjectiveResolver:

    def resolve_behavior(
        self,
        objective: SwarmObjective,
    ) -> BehaviorProfile:
        return get_profile(
            objective.type
        )


objective_resolver = ObjectiveResolver()
