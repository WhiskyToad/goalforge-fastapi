"""categories

Revision ID: 4ea087820974
Revises: ed0e10868a8b
Create Date: 2023-12-15 21:48:04.374021

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  


# revision identifiers, used by Alembic.
revision: str = '4ea087820974'
down_revision: Union[str, None] = 'ed0e10868a8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
