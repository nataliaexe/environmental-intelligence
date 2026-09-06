from datetime import datetime, timezone

from sqlalchemy import text

from app.infrastructure.database.session import engine


def test_telemetry_can_be_persisted_and_read(
    test_sensor: dict[str, str],
) -> None:

    timestamp = datetime.now(timezone.utc)

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                INSERT INTO telemetry (
                    timestamp,
                    sensor_id,
                    region_id,
                    temperature,
                    humidity,
                    soil_moisture,
                    light
                )
                VALUES (
                    :timestamp,
                    :sensor_id,
                    :region_id,
                    :temperature,
                    :humidity,
                    :soil_moisture,
                    :light
                )
                """
            ),
            {
                "timestamp": timestamp,
                "sensor_id": test_sensor["sensor_id"],
                "region_id": test_sensor["region_id"],
                "temperature": 28.5,
                "humidity": 60.0,
                "soil_moisture": 55.0,
                "light": 500.0,
            },
        )

        result = connection.execute(
            text(
                """
                SELECT
                    temperature,
                    humidity,
                    soil_moisture,
                    light
                FROM telemetry
                WHERE sensor_id = :sensor_id
                  AND timestamp = :timestamp
                """
            ),
            {
                "sensor_id": test_sensor["sensor_id"],
                "timestamp": timestamp,
            },
        ).mappings().one()

    assert result["temperature"] == 28.5
    assert result["humidity"] == 60.0
    assert result["soil_moisture"] == 55.0
    assert result["light"] == 500.0
