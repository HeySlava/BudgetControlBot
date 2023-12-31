"""Add currency

Revision ID: eae5697ecefa
Revises: 8ad3b23f1466
Create Date: 2023-07-23 00:48:01.896833

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = 'eae5697ecefa'
down_revision = '8ad3b23f1466'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('expenses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unit', sa.String(), nullable=False))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('currency', sa.String(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('currency')

    with op.batch_alter_table('expenses', schema=None) as batch_op:
        batch_op.drop_column('unit')
