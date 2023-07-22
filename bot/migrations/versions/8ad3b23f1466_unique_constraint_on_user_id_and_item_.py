"""Unique constraint on user_id and item_name

Revision ID: 8ad3b23f1466
Revises: 2565c07a5021
Create Date: 2023-07-22 16:45:37.034580

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '8ad3b23f1466'
down_revision = '2565c07a5021'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.create_unique_constraint(
                batch_op.f('uq_items_name'), ['name', 'user_id'],
            )


def downgrade() -> None:
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_items_name'), type_='unique')
