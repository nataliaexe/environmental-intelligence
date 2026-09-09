from app.domain.agent import (
    AgentLocalization,
    AgentState,
    EnvironmentalAgent,
)
from app.domain.authorization import (
    AuthorizationDecision,
    AuthorizationStatus,
)
from app.domain.mission import Mission
from app.domain.mission_state import MissionState
from app.services.missions.orchestrator import (
    mission_orchestrator,
)
from app.services.safety.evaluator import (
    mission_evaluator,
)


def build_agent() -> EnvironmentalAgent:
    return EnvironmentalAgent(
        id="CONF-AGENT-001",
        name="Confidence Test Agent",
        state=AgentState.IDLE,
        capabilities=[
            "temperature",
            "mobility",
        ],
        localization=AgentLocalization(
            x=0.0,
            y=0.0,
            z=0.0,
        ),
    )


def build_mission() -> Mission:
    return Mission(
        id="CONF-MISSION-001",
        region_id="REGION-001",
        objective="test_confidence",
        priority=0.5,
        required_capabilities=[
            "temperature",
        ],
    )


def test_low_confidence_denies_authorization() -> None:
    mission = build_mission()
    agent = build_agent()

    evaluation = mission_evaluator.evaluate(
        mission=mission,
        agent=agent,
        hazard_id="wildfire",
        risk_score=0.3,
        confidence=0.4,
    )

    assert (
        evaluation.decision.status
        == AuthorizationStatus.DENIED
    )

    assert (
        evaluation.decision.reason
        == "confidence_below_policy_minimum"
    )


def test_high_confidence_allows_authorization() -> None:
    mission = build_mission()
    agent = build_agent()

    evaluation = mission_evaluator.evaluate(
        mission=mission,
        agent=agent,
        hazard_id="drought",
        risk_score=0.3,
        confidence=0.9,
    )

    assert (
        evaluation.decision.status
        == AuthorizationStatus.AUTHORIZED
    )
