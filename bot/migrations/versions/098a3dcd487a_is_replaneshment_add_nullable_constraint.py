"""is_replaneshment add nullable constraint

Revision ID: 098a3dcd487a
Revises: 068ac5d35a1a
Create Date: 2023-07-15 23:06:35.567259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '098a3dcd487a'
down_revision = '068ac5d35a1a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('expenses', schema=None) as batch_op:
        batch_op.alter_column(
                'is_replenishment',
                existing_type=sa.BOOLEAN(),
                nullable=False,
            )


def downgrade() -> None:
    with op.batch_alter_table('expenses', schema=None) as batch_op:
        batch_op.alter_column(
                'is_replenishment',
                existing_type=sa.BOOLEAN(),
                nullable=True,
            )
