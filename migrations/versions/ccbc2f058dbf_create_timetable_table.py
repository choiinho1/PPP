"""create TimeTable table

Revision ID: ccbc2f058dbf
Revises: fa1a398992eb
Create Date: 2024-05-27 17:09:03.453152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ccbc2f058dbf'
down_revision: Union[str, None] = 'fa1a398992eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
