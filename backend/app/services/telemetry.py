from collections import deque

from app.api.schemas.telemetry import TelemetryPayload


class TelemetryStore:
    def __init__(self, max_size: int = 1000) -> None:
        self._observations: deque[TelemetryPayload] = deque(maxlen=max_size)

    def add(self, observation: TelemetryPayload) -> None:
        self._observations.append(observation)

    def latest(self, limit: int = 50) -> list[TelemetryPayload]:
        observations = list(self._observations)
        return observations[-limit:][::-1]

    def latest_by_sensor(self, sensor_id: str) -> TelemetryPayload | None:
        for observation in reversed(self._observations):
            if observation.sensor_id == sensor_id:
                return observation

        return None


telemetry_store = TelemetryStore()
