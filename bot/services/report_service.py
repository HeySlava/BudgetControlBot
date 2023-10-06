from typing import List

from data.models import Expense
from data.models import User
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_report_by_day(
        user: User,
        session: Session,
) -> List[str]:
    stmt = (
        select(
            Expense.user_id,
            func.date(Expense.cdate_tz),
            Expense.unit,
            func.sum(Expense.price).label('total'),
        )
        .where(
            Expense.user_id == user.id,
            ~Expense.is_replenishment,
        )
        .group_by(Expense.user_id, func.date(Expense.cdate_tz), Expense.unit)
    )

    rows = session.execute(stmt)
    return [f'{row.tuple()[1]}  |  {row.tuple()[3]} {row.tuple()[2]}' for row in rows]


def get_report_by_category(
        user: User,
        session: Session,
) -> List[str]:
    stmt = (
        select(
            Expense.user_id,
            Expense.item_name,
            Expense.unit,
            func.sum(Expense.price).label('total'),
        )
        .where(
            Expense.user_id == user.id,
            ~Expense.is_replenishment,
        )
        .group_by(Expense.user_id, Expense.item_name, Expense.unit)
        .order_by(Expense.item_name)
    )

    rows = session.execute(stmt)
    return [f'{row.tuple()[1]}  |  {row.tuple()[3]} {row.tuple()[2]}' for row in rows]
