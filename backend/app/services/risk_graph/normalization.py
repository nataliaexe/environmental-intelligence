RISK_HAZARD_MAP = {
    "heat_drought_stress": "heatwave",
    "extreme_heat": "heatwave",
    "drought": "drought",
    "dryness": "drought",
    "wildfire": "wildfire",
    "flood": "flood",
    "extreme_rain": "extreme_rain",
    "severe_storm": "severe_storm",
}


def normalize_hazard(
    hazard_type: str,
) -> str:

    return RISK_HAZARD_MAP.get(
        hazard_type,
        hazard_type,
    )
