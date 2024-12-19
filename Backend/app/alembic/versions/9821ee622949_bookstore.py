"""Bookstore

Revision ID: 9821ee622949
Revises: df912e9913d7
Create Date: 2024-12-19 02:36:40.464512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9821ee622949'
down_revision: Union[str, None] = 'df912e9913d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
