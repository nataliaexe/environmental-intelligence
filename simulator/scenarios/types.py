from enum import Enum


class ScenarioType(str, Enum):
    NORMAL = "normal"
    HEATWAVE = "heatwave"
    DROUGHT = "drought"
    HEAVY_RAIN = "heavy_rain"
    SENSOR_FAILURE = "sensor_failure"
    SENSOR_DRIFT = "sensor_drift"
