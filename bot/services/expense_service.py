import datetime as dt
from typing import Optional
from typing import Sequence

from config import config
from data.models import Expense
from sqlalchemy import select
from sqlalchemy.orm import Session


def add_expense(
        user_id: int,
        price: int,
        unit: str,
        session: Session,
        item_name: str,
        is_replenishment: bool = False,
        comment: Optional[str] = None,
        commit: bool = True,
) -> Expense:

    expense = Expense(
            user_id=user_id,
            item_name=item_name,
            price=price,
            unit=unit,
            comment=comment,
            is_replenishment=is_replenishment,
            cdate_tz=dt.datetime.now(config.tz),
        )
    session.add(expense)
    if commit:
        session.commit()
    return expense


def get_expenses(
        user_id: int,
        session: Session,
) -> Sequence[Expense]:
    return session.scalars(
            select(Expense).where(
                ~Expense.is_replenishment,
                Expense.user_id == user_id,
            )
        ).all()
