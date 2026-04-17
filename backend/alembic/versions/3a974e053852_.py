"""empty message

Revision ID: 3a974e053852
Revises: 487226a77cb5
Create Date: 2026-04-17 22:05:50.948833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a974e053852'
down_revision: Union[str, Sequence[str], None] = '487226a77cb5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
