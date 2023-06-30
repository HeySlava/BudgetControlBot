from sqlalchemy import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import func

from typing import List

from data.models import Expence
from data.models import User


def get_report(
        session: Session,
) -> Sequence:
    stmt = select(Expence, User).join(User, User.id == Expence.user_id)
    rows = session.execute(stmt)
    return rows


def get_report_by(
        session: Session,
        group_by=None,
) -> List[str]:
    stmt = (
            select(group_by, func.sum(Expence.price).label('total'))
            .join(User, User.id == Expence.user_id)
        )
    if group_by is not None:
        stmt = stmt.group_by(group_by)
    rows = session.execute(stmt).all()
    return [f'{row.tuple()[0]} --- {row.tuple()[1]} AMD' for row in rows]
