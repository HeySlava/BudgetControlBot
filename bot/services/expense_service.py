import datetime as dt
from typing import Sequence
from typing import Optional

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

from config import config

from data.models import Expense


def add_expense(
        user_id: int,
        item_name: str,
        price: str,
        session: Session,
        comment: Optional[str],
) -> Expense:

    expense = Expense(
            user_id=user_id,
            item_name=item_name,
            price=price,
            comment=comment,
            cdate_tz=dt.datetime.now(config.tz),
        )
    session.add(expense)
    session.commit()
    return expense


def get_expenses(
        session: Session,
) -> Sequence[Expense]:
    return session.scalars(select(Expense)).all()


def get_mean(
        session: Session,
) -> int:
    prices = session.scalars(select(Expense.price)).all()
    days = session.scalars(select(func.date(Expense.cdate_tz)).distinct()).all()
    return int(sum(prices) / len(days))
