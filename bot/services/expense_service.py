import datetime as dt
from typing import Sequence
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

from config import config
from data.models import Expense


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
        session: Session,
) -> Sequence[Expense]:
    return session.scalars(select(Expense).where(~Expense.is_replenishment)).all()


def get_expenses_by_date(
        custom_date: dt.date,
        session: Session,
) -> Sequence[Expense]:
    stmt = select(Expense).where(
            sa.and_(
                ~Expense.is_replenishment,
                func.date(Expense.cdate_tz) == custom_date,
            )
        )
    return session.scalars(stmt).all()


def get_expenses_by_item(
        item_name: str,
        session: Session,
) -> Sequence[Expense]:
    stmt = select(Expense).where(
            sa.and_(
                ~Expense.is_replenishment,
                Expense.item_name == item_name,
            )
        )
    return session.scalars(stmt).all()


def get_mean(
        session: Session,
) -> int:
    stmt = (
            select(Expense.price)
            .where(
                ~Expense.is_replenishment,
            )
        )
    prices = session.scalars(stmt).all()
    days = session.scalars(select(func.date(Expense.cdate_tz)).distinct()).all()
    return int(sum(prices) / len(days))
