from datetime import datetime, timezone

from sqlalchemy import text

from app.infrastructure.database.session import engine


def test_telemetry_can_be_persisted_and_read(
    test_sensor: dict[str, str],
) -> None:

    now = datetime.now(timezone.utc)

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
                    light,
                    occurred_at,
                    received_at,
                    processed_at
                )
                VALUES (
                    :timestamp,
                    :sensor_id,
                    :region_id,
                    :temperature,
                    :humidity,
                    :soil_moisture,
                    :light,
                    :occurred_at,
                    :received_at,
                    :processed_at
                )
                """
            ),
            {
                "timestamp": now,
                "sensor_id": test_sensor["sensor_id"],
                "region_id": test_sensor["region_id"],
                "temperature": 28.5,
                "humidity": 60.0,
                "soil_moisture": 55.0,
                "light": 500.0,
                "occurred_at": now,
                "received_at": now,
                "processed_at": now,
            },
        )

        result = connection.execute(
            text(
                """
                SELECT
                    sensor_id,
                    region_id,
                    temperature,
                    humidity,
                    soil_moisture,
                    light,
                    occurred_at,
                    received_at,
                    processed_at
                FROM telemetry
                WHERE sensor_id = :sensor_id
                ORDER BY timestamp DESC
                LIMIT 1
                """
            ),
            {
                "sensor_id": test_sensor["sensor_id"],
            },
        )

        row = result.first()

    assert row is not None

    assert row.sensor_id == test_sensor["sensor_id"]
    assert row.region_id == test_sensor["region_id"]

    assert row.temperature == 28.5
    assert row.humidity == 60.0
    assert row.soil_moisture == 55.0
    assert row.light == 500.0

    assert row.occurred_at is not None
    assert row.received_at is not None
    assert row.processed_at is not None
