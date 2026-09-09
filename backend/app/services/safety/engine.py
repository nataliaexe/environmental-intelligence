from app.domain.agent import EnvironmentalAgent
from app.domain.authorization import (
    AuthorizationDecision,
    AuthorizationStatus,
)
from app.domain.mission import Mission
from app.domain.response import ResponsePolicy


class SafetyEngine:
    def evaluate(
        self,
        mission: Mission,
        agent: EnvironmentalAgent,
        risk_score: float,
        policy: ResponsePolicy,
        confidence: float,
    ) -> AuthorizationDecision:

        if agent.trust_score < 0.5:
            return AuthorizationDecision(
                status=AuthorizationStatus.DENIED,
                reason="agent_trust_below_threshold",
                policy_id=policy.hazard_id,
            )

        if agent.energy.level < 20.0:
            return AuthorizationDecision(
                status=AuthorizationStatus.DENIED,
                reason="insufficient_agent_energy",
                policy_id=policy.hazard_id,
            )

        if confidence < policy.minimum_confidence:
            return AuthorizationDecision(
                status=AuthorizationStatus.DENIED,
                reason="confidence_below_policy_minimum",
                policy_id=policy.hazard_id,
            )

        if risk_score > policy.max_agent_risk:
            if policy.requires_human_confirmation:
                return AuthorizationDecision(
                    status=AuthorizationStatus.REQUIRES_HUMAN,
                    reason=(
                        "mission_risk_requires_human_confirmation"
                    ),
                    policy_id=policy.hazard_id,
                )

            return AuthorizationDecision(
                status=AuthorizationStatus.DENIED,
                reason=(
                    "environmental_risk_exceeds_agent_limit"
                ),
                policy_id=policy.hazard_id,
            )

        if policy.requires_human_confirmation:
            return AuthorizationDecision(
                status=AuthorizationStatus.REQUIRES_HUMAN,
                reason="policy_requires_human_confirmation",
                policy_id=policy.hazard_id,
            )

        return AuthorizationDecision(
            status=AuthorizationStatus.AUTHORIZED,
            reason="mission_passed_safety_policy",
            policy_id=policy.hazard_id,
        )


safety_engine = SafetyEngine()
