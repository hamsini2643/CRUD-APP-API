"""Add auto-increment to Person.id

Revision ID: 1084ef521af9
Revises: e1e486a2a404
Create Date: 2025-01-16 16:51:29.436698

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1084ef521af9'
down_revision: Union[str, None] = 'e1e486a2a404'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_person_id'), 'person', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_person_id'), table_name='person')
    # ### end Alembic commands ###