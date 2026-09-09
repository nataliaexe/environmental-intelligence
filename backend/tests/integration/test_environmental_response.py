from app.domain.agent import (
    AgentLocalization,
    AgentState,
    EnvironmentalAgent,
)
from app.domain.authorization import (
    AuthorizationDecision,
    AuthorizationStatus,
)
from app.domain.mission_state import MissionState
from app.infrastructure.database.dependencies import SessionLocal
from app.services.anomaly.fusion import AnomalyAssessment
from app.services.anomaly.result import DetectorResult
from app.services.environmental_response import (
    environmental_response_orchestrator,
)
from app.services.missions.orchestrator import (
    mission_orchestrator,
)


def build_high_risk_assessment() -> AnomalyAssessment:
    return AnomalyAssessment(
        anomaly=True,
        score=0.95,
        severity="critical",
        reasons=[
            "high_temperature",
            "low_humidity",
            "low_soil_moisture",
        ],
        detectors=[
            DetectorResult(
                detector="environmental_rules",
                anomaly=True,
                score=1.0,
                severity="critical",
                reasons=[
                    "high_temperature",
                    "low_humidity",
                    "low_soil_moisture",
                ],
            ),
            DetectorResult(
                detector="statistical",
                anomaly=True,
                score=0.875,
                severity="critical",
                reasons=[
                    "temperature_statistical_outlier",
                ],
            ),
        ],
    )


def build_agent() -> EnvironmentalAgent:
    return EnvironmentalAgent(
        id="TEST-AGENT-001",
        name="Test Environmental Agent 01",
        state=AgentState.IDLE,
        capabilities=[
            "temperature",
            "soil_moisture",
            "mobility",
        ],
        localization=AgentLocalization(
            x=0.0,
            y=0.0,
            z=0.0,
        ),
    )


def build_authorized_decisions(
    policy_id: str = "wildfire",
) -> list[AuthorizationDecision]:
    return [
        AuthorizationDecision(
            status=AuthorizationStatus.AUTHORIZED,
            reason="human_approved_mission",
            policy_id=policy_id,
        )
    ]


def test_environmental_response_requires_human_approval(
    test_region: str,
) -> None:
    session = SessionLocal()

    try:
        result = (
            environmental_response_orchestrator.respond(
                session=session,
                region_id=test_region,
                assessment=build_high_risk_assessment(),
                agents=[build_agent()],
                minimum_agents=1,
            )
        )

        assert result.event_id is not None
        assert result.mission is not None

        assert (
            result.status
            == "awaiting_approval"
        )

        assert (
            result.mission.status
            == MissionState.AWAITING_APPROVAL
        )

        assert result.assignment is None
        assert result.tasks == []

    finally:
        session.close()


def test_environmental_response_after_human_approval(
    test_region: str,
) -> None:
    session = SessionLocal()

    try:
        result = (
            environmental_response_orchestrator.respond(
                session=session,
                region_id=test_region,
                assessment=build_high_risk_assessment(),
                agents=[build_agent()],
                minimum_agents=1,
            )
        )

        assert result.mission is not None

        mission = result.mission

        assert (
            mission.status
            == MissionState.AWAITING_APPROVAL
        )

        approved = mission_orchestrator.approve(
            mission
        )

        assert approved is not None

        assert (
            mission.status
            == MissionState.AUTHORIZED
        )

        authorization = build_authorized_decisions(
            policy_id=result.event_id or "wildfire",
        )

        assignment = mission_orchestrator.assign(
            mission=mission,
            agents=[build_agent()],
            minimum_agents=1,
            authorization_decisions=authorization,
        )

        assert assignment is not None

        assert (
            mission.status
            == MissionState.ASSIGNED
        )

        tasks = mission_orchestrator.execute(
            mission=mission,
            agents=[build_agent()],
        )

        assert tasks

        assert (
            mission.status
            == MissionState.EXECUTING
        )

    finally:
        session.close()
