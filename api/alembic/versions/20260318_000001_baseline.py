"""baseline schema marker

Revision ID: 20260318_000001
Revises: 
Create Date: 2026-03-18

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260318_000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Baseline marker only. Existing environments can stamp this revision.
    pass


def downgrade() -> None:
    pass
