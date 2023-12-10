"""tasks initial

Revision ID: 554dadb4be53
Revises: 7682137e660b
Create Date: 2023-12-09 16:42:15.946279

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  


# revision identifiers, used by Alembic.
revision: str = '554dadb4be53'
down_revision: Union[str, None] = '7682137e660b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('recurring', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)
    op.create_index(op.f('ix_tasks_title'), 'tasks', ['title'], unique=False)
    op.create_table('task_instances',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('due_date', sa.Date(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_instances_id'), 'task_instances', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_instances_id'), table_name='task_instances')
    op.drop_table('task_instances')
    op.drop_index(op.f('ix_tasks_title'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_table('tasks')
    # ### end Alembic commands ###
