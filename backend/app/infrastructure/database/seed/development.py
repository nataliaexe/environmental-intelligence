from datetime import datetime, timezone

from sqlalchemy import select

from app.domain.agent import AgentState
from app.infrastructure.database.models import (
    AgentModel,
    RegionModel,
    SensorModel,
)
from app.infrastructure.database.session import SessionLocal


def seed() -> None:
    session = SessionLocal()

    try:
        regions = [
            RegionModel(
                id="REGION-001",
                name="North Sector",
                latitude=0.0,
                longitude=0.0,
            ),
            RegionModel(
                id="REGION-002",
                name="South Sector",
                latitude=1.0,
                longitude=1.0,
            ),
        ]

        for region in regions:
            exists = session.scalar(
                select(RegionModel).where(
                    RegionModel.id == region.id
                )
            )

            if exists is None:
                session.add(region)

        sensors = [
            SensorModel(
                id="SENSOR-001",
                region_id="REGION-001",
                name="Environmental Node 01",
                sensor_type="multi",
                status="online",
            ),
            SensorModel(
                id="SENSOR-002",
                region_id="REGION-002",
                name="Environmental Node 02",
                sensor_type="multi",
                status="online",
            ),
        ]

        for sensor in sensors:
            exists = session.scalar(
                select(SensorModel).where(
                    SensorModel.id == sensor.id
                )
            )

            if exists is None:
                session.add(sensor)

        agent = session.scalar(
            select(AgentModel).where(
                AgentModel.id == "AGENT-001"
            )
        )

        if agent is None:
            agent = AgentModel(
                id="AGENT-001",
                name="Environmental Agent 01",
                state=AgentState.IDLE.value,
                energy_level=100.0,
                energy_health=100.0,
                trust_score=1.0,
                x=0.0,
                y=0.0,
                z=0.0,
                current_mission_id=None,
            )

            session.add(agent)

        session.commit()

        print("DEVELOPMENT SEED OK")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    seed()
