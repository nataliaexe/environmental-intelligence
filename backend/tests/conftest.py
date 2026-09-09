import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.infrastructure.database.dependencies import (
    SessionLocal,
)
from app.infrastructure.database.session import engine


@pytest.fixture
def test_sensor() -> dict[str, str]:
    region_id = "TEST-REGION"
    sensor_id = "TEST-SENSOR"

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                INSERT INTO regions (
                    id,
                    name,
                    latitude,
                    longitude
                )
                VALUES (
                    :id,
                    :name,
                    :latitude,
                    :longitude
                )
                ON CONFLICT (id) DO NOTHING
                """
            ),
            {
                "id": region_id,
                "name": "Temporary Test Region",
                "latitude": 0.0,
                "longitude": 0.0,
            },
        )

        connection.execute(
            text(
                """
                INSERT INTO sensors (
                    id,
                    region_id,
                    name,
                    sensor_type,
                    status
                )
                VALUES (
                    :id,
                    :region_id,
                    :name,
                    :sensor_type,
                    :status
                )
                ON CONFLICT (id) DO NOTHING
                """
            ),
            {
                "id": sensor_id,
                "region_id": region_id,
                "name": "Temporary Test Sensor",
                "sensor_type": "multi",
                "status": "online",
            },
        )

    yield {
        "region_id": region_id,
        "sensor_id": sensor_id,
    }

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                DELETE FROM telemetry
                WHERE sensor_id = :sensor_id
                """
            ),
            {
                "sensor_id": sensor_id,
            },
        )

        connection.execute(
            text(
                """
                DELETE FROM sensors
                WHERE id = :sensor_id
                """
            ),
            {
                "sensor_id": sensor_id,
            },
        )

        connection.execute(
            text(
                """
                DELETE FROM regions
                WHERE id = :region_id
                """
            ),
            {
                "region_id": region_id,
            },
        )


@pytest.fixture
def db_session() -> Session:
    session = SessionLocal()

    try:
        yield session
        session.rollback()
    finally:
        session.close()


@pytest.fixture
def test_region() -> str:
    region_id = "TEST-REGION-CLEAN"

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                INSERT INTO regions (
                    id,
                    name,
                    latitude,
                    longitude
                )
                VALUES (
                    :id,
                    :name,
                    :latitude,
                    :longitude
                )
                ON CONFLICT (id) DO NOTHING
                """
            ),
            {
                "id": region_id,
                "name": "Clean Test Region",
                "latitude": 0.0,
                "longitude": 0.0,
            },
        )

    yield region_id

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                DELETE FROM environmental_events
                WHERE region_id = :region_id
                """
            ),
            {
                "region_id": region_id,
            },
        )

        connection.execute(
            text(
                """
                DELETE FROM risk_assessments
                WHERE region_id = :region_id
                """
            ),
            {
                "region_id": region_id,
            },
        )

        connection.execute(
            text(
                """
                DELETE FROM regions
                WHERE id = :region_id
                """
            ),
            {
                "region_id": region_id,
            },
        )
