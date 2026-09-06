import time
from datetime import datetime, timezone

import httpx

from simulator.environment import EnvironmentSimulator


API_URL = "http://127.0.0.1:8000/api/telemetry"

SENSOR_ID = "SIM-SENSOR-001"
REGION_ID = "REGION-001"


def main() -> None:
    simulator = EnvironmentSimulator(seed=42)

    print("Environmental simulator started.")
    print(f"Sensor: {SENSOR_ID}")
    print(f"Region: {REGION_ID}")
    print()

    with httpx.Client(timeout=5.0) as client:
        while True:
            state = simulator.step()

            payload = {
                "sensor_id": SENSOR_ID,
                "region_id": REGION_ID,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "temperature": round(state.temperature, 2),
                "humidity": round(state.humidity, 2),
                "soil_moisture": round(state.soil_moisture, 2),
                "light": round(state.light, 2),
            }

            response = client.post(API_URL, json=payload)
            response.raise_for_status()

            print(
                f"[SIM] "
                f"T={payload['temperature']}°C | "
                f"H={payload['humidity']}% | "
                f"Soil={payload['soil_moisture']}% | "
                f"Light={payload['light']}"
            )

            time.sleep(2)


if __name__ == "__main__":
    main()
