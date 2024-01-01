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


def get_report_by_month(
        user: User,
        session: Session,
) -> List[str]:
    by_month_year = 'month_year'
    stmt = (
        select(
            Expense.user_id,
            func.strftime('%m-%Y', Expense.cdate_tz).label(by_month_year),
            Expense.unit,
            func.sum(Expense.price).label('total'),
        )
        .where(
            Expense.user_id == user.id,
            ~Expense.is_replenishment,
        )
        .group_by(Expense.user_id, by_month_year, Expense.unit)
        .order_by(Expense.cdate_tz)
        .subquery()
    )

    return [
            f'{getattr(r, by_month_year)}  |  {r.total} {r.unit}' for
            r in
            session.execute(select(stmt))
        ]


def get_report_by_category(
        user: User,
        session: Session,
) -> List[str]:
    by_month_year = 'month_year'
    subq = (
        select(
            Expense.user_id,
            func.strftime('%m-%Y', Expense.cdate_tz).label(by_month_year),
            Expense.item_name,
            Expense.unit,
            func.sum(Expense.price).label('total'),
        )
        .where(
            Expense.user_id == user.id,
            ~Expense.is_replenishment,
        )
        .group_by(Expense.user_id, by_month_year, Expense.item_name, Expense.unit)
        .order_by(by_month_year, Expense.item_name)
        .subquery()
    )

    return [
            f'{r.item_name} ({getattr(r, by_month_year)})  |  {r.total} {r.unit}' for
            r in
            session.execute(select(subq))
        ]
