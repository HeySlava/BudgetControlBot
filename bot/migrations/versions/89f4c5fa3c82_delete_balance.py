"""Delete balance

Revision ID: 89f4c5fa3c82
Revises: 74260b1ce7a1
Create Date: 2023-07-15 22:17:19.538478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89f4c5fa3c82'
down_revision = '74260b1ce7a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('balance')


def downgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('balance', sa.INTEGER(), nullable=False))
