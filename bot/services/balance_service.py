from typing import Sequence

import sqlalchemy as sa
from data.models import Expense
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_balance_history(
        user_id: int,
        session: Session,
) -> Sequence[Expense]:

    stmt = select(Expense).where(
            Expense.is_replenishment,
            Expense.user_id == user_id,
        )
    return session.scalars(stmt).all()


def get_balance(
        user_id: int,
        session: Session,
) -> int:

    stmt = sa.select(
            sa.func.sum(
                sa.case(
                    (
                        Expense.is_replenishment,
                        Expense.price,
                    ),
                    (
                        ~Expense.is_replenishment,
                        -Expense.price,
                    )
                )
            )
        ).where(Expense.user_id == user_id)

    balance = session.execute(stmt).scalar()
    return balance if balance else 0
