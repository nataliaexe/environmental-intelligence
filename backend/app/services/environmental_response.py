from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.domain.agent import EnvironmentalAgent
from app.domain.mission import Mission
from app.domain.mission_state import MissionState
from app.services.anomaly.fusion import AnomalyAssessment
from app.services.event_engine import event_engine
from app.services.missions.orchestrator import (
    mission_orchestrator,
)
from app.services.persistence.event import (
    event_persistence,
)
from app.services.risk.propagation_service import (
    risk_propagation_service,
)


@dataclass(frozen=True)
class EnvironmentalResponseResult:

    event_id: str | None

    risk_assessments: list

    mission: Mission | None

    assignment: object | None

    tasks: list

    status: str


class EnvironmentalResponseOrchestrator:

    def respond(
        self,
        *,
        session: Session,
        region_id: str,
        assessment: AnomalyAssessment,
        agents: list[EnvironmentalAgent],
        minimum_agents: int = 1,
    ) -> EnvironmentalResponseResult:

        # -------------------------------------------------
        # 1. ANOMALY -> EVENT + INITIAL RISK
        # -------------------------------------------------

        processing = event_engine.process_with_risk(
            region_id=region_id,
            assessment=assessment,
        )

        if processing is None:
            return EnvironmentalResponseResult(
                event_id=None,
                risk_assessments=[],
                mission=None,
                assignment=None,
                tasks=[],
                status="no_anomaly",
            )

        event = processing.event
        initial_risk = processing.risk

        # -------------------------------------------------
        # 2. PERSIST EVENT
        # -------------------------------------------------

        event_persistence.create_from_event(
            session=session,
            event=event,
        )

        # -------------------------------------------------
        # 3. RISK GRAPH PROPAGATION
        # -------------------------------------------------

        risk_assessments = (
            risk_propagation_service.propagate(
                session=session,
                region_id=region_id,
                initial_hazard=(
                    initial_risk.hazard_type
                ),
                initial_score=(
                    initial_risk.risk_score
                ),
                event_id=event.id,
                initial_risk=initial_risk,
            )
        )

        # -------------------------------------------------
        # 4. CREATE MISSION
        # -------------------------------------------------

        mission = Mission(
            id=f"MISSION-{event.id}",
            region_id=region_id,
            objective=self._mission_objective(
                event.event_type
            ),
            priority=initial_risk.risk_score,
            required_capabilities=(
                self._required_capabilities(
                    event.event_type
                )
            ),
        )

        # -------------------------------------------------
        # 5. PLAN
        # -------------------------------------------------

        mission_orchestrator.create_plan(
            mission
        )

        # -------------------------------------------------
        # 6. SAFETY / AUTHORIZATION
        # -------------------------------------------------

        authorization = (
            mission_orchestrator.authorize(
                mission=mission,
                agents=agents,
                hazard_id=event.event_type,
                risk_score=initial_risk.risk_score,
                confidence=initial_risk.confidence,
            )
        )

        # -------------------------------------------------
        # 7. SWARM ASSIGNMENT
        # -------------------------------------------------

        assignment = (
            mission_orchestrator.assign(
                mission=mission,
                agents=agents,
                minimum_agents=minimum_agents,
                authorization_decisions=authorization,
            )
        )

        if assignment is None:

            if (
                mission.status
                == MissionState.AWAITING_APPROVAL
            ):
                status = "awaiting_approval"

            elif (
                mission.status
                == MissionState.BLOCKED
            ):
                status = "blocked"

            else:
                status = "assignment_failed"

            return EnvironmentalResponseResult(
                event_id=event.id,
                risk_assessments=risk_assessments,
                mission=mission,
                assignment=None,
                tasks=[],
                status=status,
            )

        # -------------------------------------------------
        # 8. EXECUTION
        # -------------------------------------------------

        tasks = mission_orchestrator.execute(
            mission=mission,
            agents=agents,
        )

        return EnvironmentalResponseResult(
            event_id=event.id,
            risk_assessments=risk_assessments,
            mission=mission,
            assignment=assignment,
            tasks=tasks,
            status="executing",
        )

    @staticmethod
    def _mission_objective(
        event_type: str,
    ) -> str:

        mapping = {
            "extreme_heat": "monitor_heat",
            "heatwave_risk": "monitor_heat",
            "heat_drought_stress": (
                "monitor_heat_drought"
            ),
            "drought": "monitor_drought",
            "drought_risk": "monitor_drought",
            "dryness": "monitor_drought",
            "wildfire": "investigate_wildfire",
            "wildfire_risk": "investigate_wildfire",
        }

        return mapping.get(
            event_type,
            "investigate_environmental_event",
        )

    @staticmethod
    def _required_capabilities(
        event_type: str,
    ) -> list[str]:

        mapping = {
            "extreme_heat": [
                "temperature",
                "mobility",
            ],
            "heatwave_risk": [
                "temperature",
                "mobility",
            ],
            "heat_drought_stress": [
                "temperature",
                "soil_moisture",
                "mobility",
            ],
            "drought": [
                "soil_moisture",
                "temperature",
                "mobility",
            ],
            "drought_risk": [
                "soil_moisture",
                "temperature",
                "mobility",
            ],
            "dryness": [
                "soil_moisture",
                "temperature",
                "mobility",
            ],
            "wildfire": [
                "smoke_detection",
                "thermal_sensing",
                "mobility",
            ],
            "wildfire_risk": [
                "smoke_detection",
                "thermal_sensing",
                "mobility",
            ],
        }

        return mapping.get(
            event_type,
            [
                "temperature",
                "mobility",
            ],
        )


environmental_response_orchestrator = (
    EnvironmentalResponseOrchestrator()
)
