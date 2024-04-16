"""added icon to task

Revision ID: 04710bfd85c4
Revises: d240ff7a3658
Create Date: 2024-04-16 12:47:24.892943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  


# revision identifiers, used by Alembic.
revision: str = '04710bfd85c4'
down_revision: Union[str, None] = 'd240ff7a3658'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('icon', sa.String(), nullable=True))
    op.create_index(op.f('ix_tasks_icon'), 'tasks', ['icon'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tasks_icon'), table_name='tasks')
    op.drop_column('tasks', 'icon')
    # ### end Alembic commands ###