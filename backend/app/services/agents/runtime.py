from dataclasses import dataclass

from app.domain.agent import EnvironmentalAgent
from simulator.swarm.agent_state import SimulatedAgent
from simulator.swarm.vector import Vector2


@dataclass
class AgentRuntime:
    domain: EnvironmentalAgent
    simulation: SimulatedAgent

    @classmethod
    def from_domain(
        cls,
        agent: EnvironmentalAgent,
    ) -> "AgentRuntime":
        return cls(
            domain=agent,
            simulation=SimulatedAgent(
                agent_id=agent.id,
                position=Vector2(
                    agent.localization.x,
                    agent.localization.y,
                ),
                energy=agent.energy.level,
            ),
        )

    def sync_to_domain(self) -> None:
        self.domain.localization.x = (
            self.simulation.position.x
        )

        self.domain.localization.y = (
            self.simulation.position.y
        )

        self.domain.energy.level = (
            self.simulation.energy
        )
