from app.domain.response import ResponsePolicy


DEFAULT_POLICIES: dict[str, ResponsePolicy] = {

    "wildfire": ResponsePolicy(
        hazard_id="wildfire",
        preferred_actions=[
            "investigate_region",
            "increase_sensor_density",
            "request_emergency_response",
        ],
        minimum_confidence=0.75,
        requires_human_confirmation=True,
        max_agent_risk=0.6,
    ),

    "flood": ResponsePolicy(
        hazard_id="flood",
        preferred_actions=[
            "increase_water_monitoring",
            "map_affected_region",
        ],
        minimum_confidence=0.70,
        requires_human_confirmation=False,
        max_agent_risk=0.7,
    ),

    "drought": ResponsePolicy(
        hazard_id="drought",
        preferred_actions=[
            "increase_monitoring",
            "request_water_assessment",
        ],
        minimum_confidence=0.65,
        requires_human_confirmation=False,
        max_agent_risk=0.8,
    ),

    "heatwave": ResponsePolicy(
        hazard_id="heatwave",
        preferred_actions=[
            "increase_monitoring",
            "request_human_attention",
        ],
        minimum_confidence=0.70,
        requires_human_confirmation=False,
        max_agent_risk=0.8,
    ),

    "earthquake": ResponsePolicy(
        hazard_id="earthquake",
        preferred_actions=[
            "increase_structural_monitoring",
            "map_affected_region",
            "request_human_attention",
        ],
        minimum_confidence=0.85,
        requires_human_confirmation=True,
        max_agent_risk=0.4,
    ),
}


def get_policy(hazard_id: str) -> ResponsePolicy:
    return DEFAULT_POLICIES.get(
        hazard_id,
        ResponsePolicy(
            hazard_id=hazard_id,
            minimum_confidence=0.8,
            requires_human_confirmation=True,
            max_agent_risk=0.3,
        ),
    )
