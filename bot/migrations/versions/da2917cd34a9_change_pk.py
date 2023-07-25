"""change pk

Revision ID: da2917cd34a9
Revises: 478804ababe8
Create Date: 2023-07-26 01:18:02.292792

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'da2917cd34a9'
down_revision = '478804ababe8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_constraint('uq_items_name', type_='unique')
        batch_op.drop_constraint('pk_items', type_='primary')
        batch_op.create_primary_key(op.f('pk_items'), ['name', 'user_id'])


def downgrade() -> None:
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_items_name', ['name', 'user_id'])
        batch_op.drop_constraint('pk_items', type_='primary')
        batch_op.create_primary_key(op.f('pk_items'), ['name'])
