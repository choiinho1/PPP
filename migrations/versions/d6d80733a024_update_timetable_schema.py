"""update TimeTable schema

Revision ID: d6d80733a024
Revises: ccbc2f058dbf
Create Date: 2024-05-27 17:14:58.755014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6d80733a024'
down_revision: Union[str, None] = 'ccbc2f058dbf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 기존 테이블 삭제
    op.drop_table('TimeTable')

    # 새 테이블 생성
    op.create_table(
        'TimeTable',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_name', sa.String(), nullable=False),
        sa.Column('event_time', sa.DateTime(), nullable=False),
        sa.Column('users', sa.String(), nullable=True),
        sa.Column('region', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # 새 테이블 삭제
    op.drop_table('TimeTable')

    # 기존 테이블 복원
    op.create_table(
        'TimeTable',
        sa.Column('event_name', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('event_name', 'user_id', 'start_date', 'end_date', 'start_time', 'end_time')
    )