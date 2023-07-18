"""Item name in expenses can be null

Revision ID: 3ce9177f3a5d
Revises: 098a3dcd487a
Create Date: 2023-07-18 23:41:38.448444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ce9177f3a5d'
down_revision = '098a3dcd487a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('expenses', schema=None) as batch_op:
        batch_op.alter_column(
                'item_name',
                existing_type=sa.VARCHAR(),
                nullable=True,
            )


def downgrade() -> None:
    with op.batch_alter_table('expenses', schema=None) as batch_op:
        batch_op.alter_column(
                'item_name',
                existing_type=sa.VARCHAR(),
                nullable=False,
            )
