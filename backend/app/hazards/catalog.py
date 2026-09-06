from app.domain.capability import Capability
from app.domain.hazard import HazardDefinition, HazardDomain


HAZARDS: dict[str, HazardDefinition] = {

    "heatwave": HazardDefinition(
        id="heatwave",
        name="Extreme Heat / Heatwave",
        domain=HazardDomain.HYDROMETEOROLOGICAL,
        description=(
            "Prolonged or unusually intense heat "
            "affecting an environmental region."
        ),
        required_observations=[
            "temperature",
            "humidity",
            "historical_temperature",
        ],
        compatible_capabilities=[
            Capability.TEMPERATURE,
            Capability.HUMIDITY,
        ],
        possible_actions=[
            "increase_monitoring",
            "request_human_attention",
        ],
    ),

    "drought": HazardDefinition(
        id="drought",
        name="Drought",
        domain=HazardDomain.HYDROMETEOROLOGICAL,
        description=(
            "Persistent water deficit affecting environmental systems."
        ),
        required_observations=[
            "soil_moisture",
            "precipitation",
            "temperature",
            "water_availability",
        ],
        compatible_capabilities=[
            Capability.SOIL_MOISTURE,
            Capability.TEMPERATURE,
            Capability.WATER_LEVEL,
        ],
        possible_actions=[
            "increase_monitoring",
            "activate_irrigation",
            "request_water_assessment",
        ],
    ),

    "flood": HazardDefinition(
        id="flood",
        name="Flood",
        domain=HazardDomain.HYDROMETEOROLOGICAL,
        description=(
            "Water accumulation or overflow affecting normally "
            "non-submerged areas."
        ),
        required_observations=[
            "water_level",
            "rainfall",
            "water_flow",
        ],
        compatible_capabilities=[
            Capability.WATER_LEVEL,
            Capability.WATER_FLOW,
            Capability.PRESSURE,
            Capability.MOBILITY,
        ],
        possible_actions=[
            "increase_water_monitoring",
            "map_affected_region",
            "request_human_attention",
        ],
    ),

    "wildfire": HazardDefinition(
        id="wildfire",
        name="Wildfire",
        domain=HazardDomain.ENVIRONMENTAL,
        description=(
            "Uncontrolled vegetation fire requiring environmental "
            "monitoring and response coordination."
        ),
        required_observations=[
            "temperature",
            "humidity",
            "smoke",
            "thermal_signal",
        ],
        compatible_capabilities=[
            Capability.TEMPERATURE,
            Capability.HUMIDITY,
            Capability.SMOKE_DETECTION,
            Capability.THERMAL_SENSING,
            Capability.VISUAL_SENSING,
            Capability.MOBILITY,
        ],
        possible_actions=[
            "investigate_region",
            "increase_sensor_density",
            "request_emergency_response",
        ],
    ),

    "severe_storm": HazardDefinition(
        id="severe_storm",
        name="Severe Storm",
        domain=HazardDomain.HYDROMETEOROLOGICAL,
        description=(
            "Severe atmospheric event involving combinations of "
            "wind, precipitation and pressure changes."
        ),
        required_observations=[
            "pressure",
            "wind",
            "rainfall",
        ],
        compatible_capabilities=[
            Capability.PRESSURE,
            Capability.WATER_LEVEL,
            Capability.MOBILITY,
        ],
        possible_actions=[
            "increase_monitoring",
            "request_human_attention",
        ],
    ),

    "earthquake": HazardDefinition(
        id="earthquake",
        name="Earthquake",
        domain=HazardDomain.GEOLOGICAL,
        description=(
            "Seismic event producing ground motion."
        ),
        required_observations=[
            "ground_vibration",
            "acceleration",
        ],
        compatible_capabilities=[
            Capability.VIBRATION,
            Capability.ACCELEROMETER,
            Capability.LOCALIZATION,
        ],
        possible_actions=[
            "increase_structural_monitoring",
            "map_affected_region",
            "request_human_attention",
        ],
    ),

    "landslide": HazardDefinition(
        id="landslide",
        name="Landslide",
        domain=HazardDomain.GEOLOGICAL,
        description=(
            "Downward movement of soil, rock or debris."
        ),
        required_observations=[
            "ground_motion",
            "soil_moisture",
            "slope",
            "rainfall",
        ],
        compatible_capabilities=[
            Capability.SOIL_MOISTURE,
            Capability.ACCELEROMETER,
            Capability.VISUAL_SENSING,
            Capability.LOCALIZATION,
        ],
        possible_actions=[
            "increase_monitoring",
            "investigate_region",
            "request_human_attention",
        ],
    ),

    "chemical_contamination": HazardDefinition(
        id="chemical_contamination",
        name="Chemical Contamination",
        domain=HazardDomain.CHEMICAL,
        description=(
            "Detection of potentially hazardous chemical conditions "
            "in an environmental region."
        ),
        required_observations=[
            "gas_concentration",
            "air_quality",
        ],
        compatible_capabilities=[
            Capability.GAS_DETECTION,
            Capability.AIR_QUALITY,
            Capability.MOBILITY,
        ],
        possible_actions=[
            "isolate_region",
            "request_specialized_response",
        ],
    ),

    "air_pollution": HazardDefinition(
        id="air_pollution",
        name="Air Pollution",
        domain=HazardDomain.ENVIRONMENTAL,
        description=(
            "Degraded atmospheric conditions detected through "
            "environmental measurements."
        ),
        required_observations=[
            "air_quality",
            "particulate_measurement",
        ],
        compatible_capabilities=[
            Capability.AIR_QUALITY,
            Capability.MOBILITY,
        ],
        possible_actions=[
            "increase_monitoring",
            "map_affected_region",
        ],
    ),

    "biological_outbreak": HazardDefinition(
        id="biological_outbreak",
        name="Biological Hazard",
        domain=HazardDomain.BIOLOGICAL,
        description=(
            "Detection of biological conditions requiring "
            "specialized environmental monitoring."
        ),
        required_observations=[
            "biological_indicator",
            "environmental_conditions",
        ],
        compatible_capabilities=[
            Capability.VISUAL_SENSING,
            Capability.TEMPERATURE,
            Capability.HUMIDITY,
        ],
        possible_actions=[
            "increase_monitoring",
            "request_specialized_response",
        ],
    ),

    "solar_storm": HazardDefinition(
        id="solar_storm",
        name="Solar / Space Weather Event",
        domain=HazardDomain.EXTRATERRESTRIAL,
        description=(
            "Space-weather event potentially affecting technological "
            "and communication infrastructure."
        ),
        required_observations=[
            "space_weather",
            "communication_health",
        ],
        compatible_capabilities=[
            Capability.COMMUNICATION_RELAY,
        ],
        possible_actions=[
            "switch_to_local_mode",
            "increase_system_resilience",
        ],
    ),

    "infrastructure_failure": HazardDefinition(
        id="infrastructure_failure",
        name="Infrastructure Failure",
        domain=HazardDomain.TECHNOLOGICAL,
        description=(
            "Failure of infrastructure relevant to environmental "
            "monitoring or response."
        ),
        required_observations=[
            "device_health",
            "network_health",
        ],
        compatible_capabilities=[
            Capability.COMMUNICATION_RELAY,
            Capability.LOCALIZATION,
        ],
        possible_actions=[
            "reroute_communication",
            "reassign_agents",
            "switch_to_local_mode",
        ],
    ),

}
