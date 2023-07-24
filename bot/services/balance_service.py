from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from data.models import Expense


def get_balance_history(
        user_id: int,
        session: Session,
) -> Sequence[Expense]:

    stmt = select(Expense).where(
            Expense.is_replenishment,
            Expense.user_id == user_id,
        )
    return session.scalars(stmt).all()
