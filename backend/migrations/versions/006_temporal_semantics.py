"""add telemetry temporal semantics

Revision ID: 006_temporal
Revises: 005_add_anomaly_source_model
Create Date: 2026-09-09

"""
from alembic import op
import sqlalchemy as sa


revision = "006_temporal"
down_revision = "005_add_anomaly_source_model"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "telemetry",
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "telemetry",
        sa.Column(
            "received_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.add_column(
        "telemetry",
        sa.Column(
            "processed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.execute(
        """
        UPDATE telemetry
        SET occurred_at = timestamp
        WHERE occurred_at IS NULL
        """
    )

    op.execute(
        """
        UPDATE telemetry
        SET received_at = timestamp
        WHERE received_at IS NULL
        """
    )

    op.alter_column(
        "telemetry",
        "occurred_at",
        nullable=False,
    )

    op.alter_column(
        "telemetry",
        "received_at",
        nullable=False,
    )

    op.create_index(
        "ix_telemetry_occurred_at",
        "telemetry",
        ["occurred_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_telemetry_occurred_at",
        table_name="telemetry",
    )

    op.drop_column("telemetry", "processed_at")
    op.drop_column("telemetry", "received_at")
    op.drop_column("telemetry", "occurred_at")
