"""tasks fix

Revision ID: 401f4d2c3291
Revises: 554dadb4be53
Create Date: 2023-12-09 16:48:24.117679

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  


# revision identifiers, used by Alembic.
revision: str = '401f4d2c3291'
down_revision: Union[str, None] = '554dadb4be53'
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