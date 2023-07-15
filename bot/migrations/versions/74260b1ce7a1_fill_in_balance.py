"""Fill in balance

Revision ID: 74260b1ce7a1
Revises: 25b6523cb85d
Create Date: 2023-07-15 15:44:52.608824

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm

from data.models import Expense
from data.models import User


# revision identifiers, used by Alembic.
revision = '74260b1ce7a1'
down_revision = '25b6523cb85d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    session = orm.Session(bind=op.get_bind())
    subquery = (
            sa.select(
                Expense.user_id, sa.func.sum(Expense.price).label('total')
            )
            .group_by(Expense.user_id)
            .subquery()
        )

    update_stmt = (
            sa.update(User).values(balance=-subquery.c.total)
            .where(User.id == subquery.c.user_id)
        )
    session.execute(update_stmt)
    session.commit()


def downgrade() -> None:
    session = orm.Session(bind=op.get_bind())
    session.execute(sa.update(User).values(balance=0))
    session.commit()
