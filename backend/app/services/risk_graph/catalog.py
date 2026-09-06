from app.services.risk_graph.model import (
    RiskEdge,
    RiskGraph,
)


RISK_GRAPH = RiskGraph(
    nodes={
        "heatwave",
        "drought",
        "wildfire",
        "flood",
        "landslide",
        "air_pollution",
        "extreme_rain",
        "severe_storm",
        "communication_failure",
    },

    edges=[

        RiskEdge(
            source="heatwave",
            target="drought",
            probability_multiplier=1.35,
            description=(
                "Persistent extreme heat can increase "
                "water stress."
            ),
        ),

        RiskEdge(
            source="heatwave",
            target="wildfire",
            probability_multiplier=1.50,
            description=(
                "Extreme heat can increase wildfire risk "
                "under suitable environmental conditions."
            ),
        ),

        RiskEdge(
            source="drought",
            target="wildfire",
            probability_multiplier=1.45,
            description=(
                "Dry environmental conditions can increase "
                "wildfire susceptibility."
            ),
        ),

        RiskEdge(
            source="extreme_rain",
            target="flood",
            probability_multiplier=1.60,
            description=(
                "Extreme rainfall can rapidly increase "
                "flood risk."
            ),
        ),

        RiskEdge(
            source="extreme_rain",
            target="landslide",
            probability_multiplier=1.40,
            description=(
                "Heavy rainfall can increase slope instability."
            ),
        ),

        RiskEdge(
            source="flood",
            target="communication_failure",
            probability_multiplier=1.15,
            description=(
                "Flooding can damage or disrupt communication "
                "infrastructure."
            ),
        ),

        RiskEdge(
            source="wildfire",
            target="air_pollution",
            probability_multiplier=1.55,
            description=(
                "Wildfire smoke can degrade air quality."
            ),
        ),

        RiskEdge(
            source="severe_storm",
            target="flood",
            probability_multiplier=1.30,
            description=(
                "Severe storms may increase flood conditions."
            ),
        ),
    ],
)
