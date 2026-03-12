import datetime as dt
from typing import List
from typing import Sequence
from typing import Tuple

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
    stmt = (
        select(
            Expense.item_name,
            Expense.unit,
            func.sum(Expense.price).label('total'),
        )
        .where(
            Expense.user_id == user.id,
            ~Expense.is_replenishment,
        )
        .group_by(Expense.item_name, Expense.unit)
        .order_by(Expense.item_name)
    )

    return [
            f'{r.item_name}  |  {r.total} {r.unit}' for
            r in
            session.execute(stmt)
        ]


def get_months_summary(
        user: User,
        session: Session,
) -> List[Tuple[str, int, str]]:
    by_month_year = 'month_year'
    stmt = (
        select(
            func.strftime('%Y-%m', Expense.cdate_tz).label(by_month_year),
            Expense.unit,
            func.sum(Expense.price).label('total'),
        )
        .where(
            Expense.user_id == user.id,
            ~Expense.is_replenishment,
        )
        .group_by(by_month_year, Expense.unit)
        .order_by(func.strftime('%Y-%m', Expense.cdate_tz).desc())
    )
    rows = session.execute(stmt).all()
    by_month: dict = {}
    for r in rows:
        key = getattr(r, by_month_year)
        if key not in by_month:
            by_month[key] = [0, r.unit]
        by_month[key][0] += r.total
    return [(k, v[0], v[1]) for k, v in sorted(by_month.items(), reverse=True)]


def get_month_total(
        user: User,
        month_year: str,
        session: Session,
) -> Tuple[int, str]:
    stmt = (
        select(Expense.unit, func.sum(Expense.price).label('total'))
        .where(
            Expense.user_id == user.id,
            ~Expense.is_replenishment,
            func.strftime('%Y-%m', Expense.cdate_tz) == month_year,
        )
        .group_by(Expense.unit)
    )
    rows = session.execute(stmt).all()
    total = sum(r.total for r in rows)
    unit = rows[0].unit if rows else ''
    return (total, unit)


def get_month_categories(
        user: User,
        month_year: str,
        session: Session,
) -> List[Tuple[str, int, str]]:
    stmt = (
        select(
            Expense.item_name,
            Expense.unit,
            func.sum(Expense.price).label('total'),
        )
        .where(
            Expense.user_id == user.id,
            ~Expense.is_replenishment,
            func.strftime('%Y-%m', Expense.cdate_tz) == month_year,
        )
        .group_by(Expense.item_name, Expense.unit)
        .order_by(func.sum(Expense.price).desc())
    )
    rows = session.execute(stmt).all()
    return [(r.item_name or '—', r.total, r.unit) for r in rows]


def get_category_details(
        user: User,
        month_year: str,
        item_name: str,
        session: Session,
) -> Sequence[Expense]:
    stmt = (
        select(Expense)
        .where(
            Expense.user_id == user.id,
            ~Expense.is_replenishment,
            func.strftime('%Y-%m', Expense.cdate_tz) == month_year,
            Expense.item_name == item_name,
        )
        .order_by(Expense.cdate_tz)
    )
    return session.scalars(stmt).all()


def get_category_by_day(
        user: User,
        month_year: str,
        item_name: str,
        session: Session,
) -> List[Tuple[dt.date, int, str]]:
    stmt = (
        select(
            func.date(Expense.cdate_tz).label('d'),
            Expense.unit,
            func.sum(Expense.price).label('total'),
        )
        .where(
            Expense.user_id == user.id,
            ~Expense.is_replenishment,
            func.strftime('%Y-%m', Expense.cdate_tz) == month_year,
            Expense.item_name == item_name,
        )
        .group_by(func.date(Expense.cdate_tz), Expense.unit)
    )
    rows = session.execute(stmt).all()
    by_date: dict = {}
    for r in rows:
        d = (
            dt.datetime.strptime(r.d, '%Y-%m-%d').date()
            if isinstance(r.d, str)
            else r.d
        )
        if d not in by_date:
            by_date[d] = [0, r.unit]
        by_date[d][0] += r.total
    return [(d, t[0], t[1]) for d, t in sorted(by_date.items())]


def get_day_details(
        user: User,
        date: dt.date,
        session: Session,
) -> Sequence[Expense]:
    stmt = (
        select(Expense)
        .where(
            Expense.user_id == user.id,
            ~Expense.is_replenishment,
            func.date(Expense.cdate_tz) == date,
        )
        .order_by(Expense.cdate_tz)
    )
    return session.scalars(stmt).scalars().all()
