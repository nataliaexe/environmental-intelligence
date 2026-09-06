from dataclasses import dataclass

from app.domain.agent import EnvironmentalAgent
from app.domain.authorization import (
    AuthorizationDecision,
)
from app.domain.mission import Mission
from app.services.safety.engine import safety_engine
from app.services.safety.policies import get_policy


@dataclass(frozen=True)
class MissionEvaluation:
    agent_id: str
    mission_id: str
    decision: AuthorizationDecision


class MissionEvaluator:
    def evaluate(
        self,
        mission: Mission,
        agent: EnvironmentalAgent,
        hazard_id: str,
        risk_score: float,
    ) -> MissionEvaluation:
        policy = get_policy(hazard_id)

        decision = safety_engine.evaluate(
            mission=mission,
            agent=agent,
            risk_score=risk_score,
            policy=policy,
        )

        return MissionEvaluation(
            agent_id=agent.id,
            mission_id=mission.id,
            decision=decision,
        )


mission_evaluator = MissionEvaluator()
