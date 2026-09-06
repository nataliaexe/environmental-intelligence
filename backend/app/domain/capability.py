from enum import Enum


class Capability(str, Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    SOIL_MOISTURE = "soil_moisture"
    LIGHT = "light"

    WATER_LEVEL = "water_level"
    WATER_FLOW = "water_flow"
    PRESSURE = "pressure"

    SMOKE_DETECTION = "smoke_detection"
    AIR_QUALITY = "air_quality"
    GAS_DETECTION = "gas_detection"

    THERMAL_SENSING = "thermal_sensing"
    VISUAL_SENSING = "visual_sensing"
    ACOUSTIC_SENSING = "acoustic_sensing"

    VIBRATION = "vibration"
    ACCELEROMETER = "accelerometer"

    GNSS = "gnss"
    LOCALIZATION = "localization"

    MOBILITY = "mobility"
    MAGNETIC_COUPLING = "magnetic_coupling"

    IRRIGATION = "irrigation"
    WATER_SAMPLING = "water_sampling"

    COMMUNICATION_RELAY = "communication_relay"
