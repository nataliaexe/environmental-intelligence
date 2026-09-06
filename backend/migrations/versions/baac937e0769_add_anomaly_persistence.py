"""add anomaly persistence

Revision ID: baac937e0769
Revises: 19f010aeaf58
Create Date: 2026-09-06 06:41:06.676741

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "baac937e0769"
down_revision: Union[str, Sequence[str], None] = "19f010aeaf58"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "anomalies",
        sa.Column(
            "id",
            sa.String(length=64),
            nullable=False,
        ),
        sa.Column(
            "region_id",
            sa.String(length=64),
            nullable=False,
        ),
        sa.Column(
            "sensor_id",
            sa.String(length=64),
            nullable=False,
        ),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "anomaly_type",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "severity",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "score",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.String(length=1000),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["region_id"],
            ["regions.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_anomalies_region_id",
        "anomalies",
        ["region_id"],
        unique=False,
    )

    op.create_index(
        "ix_anomalies_sensor_id",
        "anomalies",
        ["sensor_id"],
        unique=False,
    )

    op.create_index(
        "ix_anomalies_timestamp",
        "anomalies",
        ["timestamp"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_anomalies_timestamp",
        table_name="anomalies",
    )

    op.drop_index(
        "ix_anomalies_sensor_id",
        table_name="anomalies",
    )

    op.drop_index(
        "ix_anomalies_region_id",
        table_name="anomalies",
    )

    op.drop_table("anomalies")
