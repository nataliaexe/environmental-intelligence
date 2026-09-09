from dataclasses import dataclass

from app.domain.agent import EnvironmentalAgent


@dataclass
class AgentRuntime:
    domain: EnvironmentalAgent
    position_x: float
    position_y: float
    energy: float

    @classmethod
    def from_domain(
        cls,
        agent: EnvironmentalAgent,
    ) -> "AgentRuntime":
        return cls(
            domain=agent,
            position_x=agent.localization.x,
            position_y=agent.localization.y,
            energy=agent.energy.level,
        )

    def sync_to_domain(self) -> None:
        self.domain.localization.x = (
            self.position_x
        )

        self.domain.localization.y = (
            self.position_y
        )

        self.domain.energy.level = (
            self.energy
        )
