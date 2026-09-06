from dataclasses import dataclass, field

from simulator.swarm.agent_state import SimulatedAgent
from simulator.swarm.behavior_profile import BehaviorProfile
from simulator.swarm.behaviors.combined import calculate_acceleration
from simulator.swarm.config import SwarmConfig
from simulator.swarm.vector import Vector2
from simulator.swarm.world import SwarmWorld


@dataclass
class SwarmSimulation:
    world: SwarmWorld

    agents: list[SimulatedAgent] = field(
        default_factory=list
    )

    config: SwarmConfig = field(
        default_factory=SwarmConfig
    )

    behavior_profile: BehaviorProfile | None = None

    time: float = 0.0

    def _neighbors(
        self,
        agent: SimulatedAgent,
    ) -> list[SimulatedAgent]:
        return [
            other
            for other in self.agents
            if other is not agent
            and other.active
            and agent.position.distance_to(
                other.position
            ) <= self.config.neighbor_radius
        ]

    def step(
        self,
        dt: float = 1.0,
    ) -> None:
        accelerations: dict[str, Vector2] = {}

        for agent in self.agents:
            if not agent.active:
                continue

            neighbors = self._neighbors(agent)

            accelerations[agent.agent_id] = (
                calculate_acceleration(
                    agent=agent,
                    neighbors=neighbors,
                    world=self.world,
                    config=self.config,
                    behavior_profile=self.behavior_profile,
                )
            )

        for agent in self.agents:
            if not agent.active:
                continue

            agent.acceleration = accelerations[
                agent.agent_id
            ]

            agent.velocity += (
                agent.acceleration * dt
            )

            speed = agent.velocity.magnitude()

            if speed > agent.max_speed:
                agent.velocity = (
                    agent.velocity.normalized()
                    * agent.max_speed
                )

            agent.position += (
                agent.velocity * dt
            )

            self._keep_inside_world(agent)

            agent.energy = max(
                0.0,
                agent.energy
                - self.config.energy_per_step,
            )

            if agent.energy <= 0:
                agent.active = False

        self.time += dt

    def _keep_inside_world(
        self,
        agent: SimulatedAgent,
    ) -> None:
        agent.position.x = max(
            0.0,
            min(
                self.world.width,
                agent.position.x,
            ),
        )

        agent.position.y = max(
            0.0,
            min(
                self.world.height,
                agent.position.y,
            ),
        )
