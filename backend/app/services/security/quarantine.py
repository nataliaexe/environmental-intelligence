from app.domain.agent import AgentState, EnvironmentalAgent


class QuarantineService:
    def quarantine(
        self,
        agent: EnvironmentalAgent,
    ) -> None:
        agent.state = AgentState.QUARANTINED
        agent.trust_score = 0.0

    def revoke(
        self,
        agent: EnvironmentalAgent,
    ) -> None:
        agent.state = AgentState.QUARANTINED
        agent.trust_score = 0.0


quarantine_service = QuarantineService()
