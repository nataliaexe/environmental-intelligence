from dataclasses import dataclass

from app.domain.agent import AgentState, EnvironmentalAgent
from app.domain.mission import Mission


@dataclass(frozen=True)
class AgentMatch:
    agent_id: str
    score: float
    reasons: list[str]


class AgentMatcher:
    def match(
        self,
        mission: Mission,
        agents: list[EnvironmentalAgent],
    ) -> list[AgentMatch]:
        matches: list[AgentMatch] = []

        required = set(mission.required_capabilities)

        for agent in agents:
            if agent.state != AgentState.IDLE:
                continue

            if agent.energy.level < 20.0:
                continue

            if agent.trust_score < 0.5:
                continue

            capabilities = set(agent.capabilities)

            missing = required - capabilities

            if missing:
                continue

            score = 0.0
            reasons: list[str] = []

            score += 0.4
            reasons.append("idle")

            score += min(agent.energy.level / 100.0, 1.0) * 0.2

            if agent.trust_score >= 0.9:
                score += 0.2
                reasons.append("high_trust")
            elif agent.trust_score >= 0.75:
                score += 0.1
                reasons.append("acceptable_trust")

            score += min(len(capabilities) / 10.0, 0.2)

            reasons.append("capabilities_match")

            matches.append(
                AgentMatch(
                    agent_id=agent.id,
                    score=round(min(score, 1.0), 4),
                    reasons=reasons,
                )
            )

        matches.sort(
            key=lambda match: match.score,
            reverse=True,
        )

        return matches


agent_matcher = AgentMatcher()
