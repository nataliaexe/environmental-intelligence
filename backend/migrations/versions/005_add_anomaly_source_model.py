"""add anomaly source model

Revision ID: 005_add_anomaly_source_model
Revises: baac937e0769
Create Date: 2026-09-09

"""
from alembic import op
import sqlalchemy as sa


revision = "005_add_anomaly_source_model"
down_revision = "baac937e0769"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "anomalies",
        sa.Column(
            "source_type",
            sa.String(50),
            nullable=False,
            server_default="sensor",
        ),
    )

    op.add_column(
        "anomalies",
        sa.Column(
            "source_id",
            sa.String(64),
            nullable=False,
            server_default="unknown",
        ),
    )

    op.create_index(
        "ix_anomalies_source_type",
        "anomalies",
        ["source_type"],
    )

    op.create_index(
        "ix_anomalies_source_id",
        "anomalies",
        ["source_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_anomalies_source_id",
        table_name="anomalies",
    )

    op.drop_index(
        "ix_anomalies_source_type",
        table_name="anomalies",
    )

    op.drop_column("anomalies", "source_id")
    op.drop_column("anomalies", "source_type")
