"""Set balance is not nullable

Revision ID: 25b6523cb85d
Revises: 6097111416de
Create Date: 2023-07-15 14:19:17.436180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25b6523cb85d'
down_revision = '6097111416de'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column(
                'balance',
                existing_type=sa.INTEGER(),
                nullable=False,
            )


def downgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column(
                'balance',
                existing_type=sa.INTEGER(),
                nullable=True,
            )
