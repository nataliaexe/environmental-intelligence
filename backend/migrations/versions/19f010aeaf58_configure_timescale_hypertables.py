"""configure timescale hypertables

Revision ID: 19f010aeaf58
Revises: 973a78b76f36
Create Date: 2026-09-06

"""
from typing import Sequence, Union

from alembic import op


revision: str = "19f010aeaf58"
down_revision: Union[str, Sequence[str], None] = "973a78b76f36"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        SELECT create_hypertable(
            'telemetry',
            by_range('timestamp'),
            if_not_exists => TRUE
        )
        """
    )

    op.execute(
        """
        SELECT create_hypertable(
            'agent_position_history',
            by_range('timestamp'),
            if_not_exists => TRUE
        )
        """
    )


def downgrade() -> None:
    raise NotImplementedError(
        "Hypertable removal must be handled explicitly."
    )
