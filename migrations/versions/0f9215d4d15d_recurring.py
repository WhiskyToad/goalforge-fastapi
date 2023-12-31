"""recurring

Revision ID: 0f9215d4d15d
Revises: 82714836089e
Create Date: 2023-12-15 11:36:56.567283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  


# revision identifiers, used by Alembic.
revision: str = '0f9215d4d15d'
down_revision: Union[str, None] = '82714836089e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('recurring_interval', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'recurring_interval')
    # ### end Alembic commands ###
