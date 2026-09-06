from app.domain.agent import (
    AgentState,
    EnvironmentalAgent,
)


def test_environmental_agent_defaults() -> None:
    agent = EnvironmentalAgent(
        id="TEST-001",
        name="Test Agent",
    )

    assert agent.state == AgentState.IDLE
    assert agent.energy.level == 100.0
    assert agent.energy.health == 100.0
    assert agent.trust_score == 1.0
