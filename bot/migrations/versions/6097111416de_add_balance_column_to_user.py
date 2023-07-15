"""Add balance column to user

Revision ID: 6097111416de
Revises: 64e5dbe5b607
Create Date: 2023-07-15 13:48:09.817420

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

from data.models import User


# revision identifiers, used by Alembic.
revision = '6097111416de'
down_revision = '64e5dbe5b607'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('balance', sa.Integer(), nullable=True))

    session = Session(bind=op.get_bind())
    stmt = (
            sa.update(User)
            .where(User.balance == None)  # noqa: E711
            .values(balance=0)
        )

    session.execute(stmt)
    session.commit()


def downgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('balance')
