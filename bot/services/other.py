from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import func

from typing import List

from data.models import Expense
from data.models import Item
from data.models import User


def get_report_by(
        session: Session,
        group_by=None,
) -> List[str]:
    stmt = (
        select(group_by, func.sum(Expense.price).label('total'))
        .join(User, User.id == Expense.user_id)
        .join(Item, Item.name == Expense.item_name)
    )

    if group_by is not None:
        stmt = stmt.group_by(group_by)
        rows = session.execute(stmt)
    return [f'{row.tuple()[0]}  |  {row.tuple()[1]} AMD' for row in rows]
