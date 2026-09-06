from simulator.swarm.agent_state import SimulatedAgent
from simulator.swarm.behavior_profile import BehaviorProfile
from simulator.swarm.config import SwarmConfig
from simulator.swarm.vector import Vector2

from simulator.swarm.behaviors.alignment import alignment
from simulator.swarm.behaviors.cohesion import cohesion
from simulator.swarm.behaviors.obstacles import obstacle_avoidance
from simulator.swarm.behaviors.separation import separation
from simulator.swarm.behaviors.target import target_attraction
from simulator.swarm.world import SwarmWorld


def calculate_acceleration(
    agent: SimulatedAgent,
    neighbors: list[SimulatedAgent],
    world: SwarmWorld,
    config: SwarmConfig,
    behavior_profile: BehaviorProfile | None = None,
) -> Vector2:

    profile = behavior_profile or BehaviorProfile(
        separation_weight=config.separation_weight,
        alignment_weight=config.alignment_weight,
        cohesion_weight=config.cohesion_weight,
        target_weight=config.target_weight,
        obstacle_weight=config.obstacle_weight,
    )

    separation_force = separation(
        agent,
        neighbors,
        config.separation_radius,
    )

    alignment_force = alignment(
        agent,
        neighbors,
    )

    cohesion_force = cohesion(
        agent,
        neighbors,
    )

    target = (
        agent.navigation_target
        if agent.navigation_target is not None
        else world.target
    )

    target_force = target_attraction(
        agent.position,
        target,
    )

    obstacle_force = obstacle_avoidance(
        agent,
        world.obstacles,
    )

    acceleration = (
        separation_force * profile.separation_weight
        + alignment_force * profile.alignment_weight
        + cohesion_force * profile.cohesion_weight
        + target_force * profile.target_weight
        + obstacle_force * profile.obstacle_weight
    )

    magnitude = acceleration.magnitude()

    if magnitude > config.max_acceleration:
        acceleration = (
            acceleration.normalized()
            * config.max_acceleration
        )

    return acceleration
