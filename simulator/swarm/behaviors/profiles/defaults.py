from simulator.swarm.behavior_profile import BehaviorProfile


PROFILES: dict[str, BehaviorProfile] = {

    "investigate": BehaviorProfile(
        separation_weight=1.8,
        alignment_weight=0.7,
        cohesion_weight=1.2,
        target_weight=2.0,
        obstacle_weight=2.5,
    ),

    "increase_coverage": BehaviorProfile(
        separation_weight=2.2,
        alignment_weight=0.8,
        cohesion_weight=0.3,
        target_weight=0.8,
        obstacle_weight=2.5,
    ),

    "map_region": BehaviorProfile(
        separation_weight=1.8,
        alignment_weight=1.0,
        cohesion_weight=0.5,
        target_weight=0.9,
        obstacle_weight=2.5,
    ),

    "create_relay": BehaviorProfile(
        separation_weight=1.2,
        alignment_weight=1.2,
        cohesion_weight=1.5,
        target_weight=1.0,
        obstacle_weight=2.5,
    ),

    "emergency": BehaviorProfile(
        separation_weight=2.5,
        alignment_weight=1.0,
        cohesion_weight=1.4,
        target_weight=2.5,
        obstacle_weight=3.0,
    ),
}


def get_profile(
    objective_type: str,
) -> BehaviorProfile:
    return PROFILES.get(
        objective_type,
        PROFILES["increase_coverage"],
    )
