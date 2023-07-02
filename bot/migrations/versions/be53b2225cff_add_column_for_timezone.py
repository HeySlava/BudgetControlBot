"""Add column for timezone

Revision ID: be53b2225cff
Revises: 6d89a09f1d69
Create Date: 2023-07-02 22:28:41.478988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be53b2225cff'
down_revision = '6d89a09f1d69'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('expenses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cdate_tz', sa.DateTime(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('expenses', schema=None) as batch_op:
        batch_op.drop_column('cdate_tz')
