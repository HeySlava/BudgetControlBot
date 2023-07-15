"""Add column is_replaneshment

Revision ID: 7bd213a55a87
Revises: 89f4c5fa3c82
Create Date: 2023-07-15 22:56:32.037417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bd213a55a87'
down_revision = '89f4c5fa3c82'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('expenses', schema=None) as batch_op:
        batch_op.add_column(
                sa.Column('is_replenishment', sa.Boolean(), nullable=True)
            )


def downgrade() -> None:
    with op.batch_alter_table('expenses', schema=None) as batch_op:
        batch_op.drop_column('is_replenishment')
