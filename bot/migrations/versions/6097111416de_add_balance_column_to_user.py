"""Add balance column to user

Revision ID: 6097111416de
Revises: 64e5dbe5b607
Create Date: 2023-07-15 13:48:09.817420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6097111416de'
down_revision = '64e5dbe5b607'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('balance', sa.Integer(), nullable=True))

    stmt = 'UPDATE users SET balance=0 WHERE users.balance IS NULL'
    op.execute(stmt)


def downgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('balance')
