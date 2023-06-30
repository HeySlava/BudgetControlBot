from typing import Sequence

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

from data.models import Expence


def add_expence(
        user_id: int,
        item_name: str,
        price: str,
        session: Session,
) -> Expence:

    expence = Expence(
            user_id=user_id,
            item_name=item_name,
            price=price,
        )
    session.add(expence)
    session.commit()
    return expence


def get_expences(
        session: Session,
) -> Sequence[Expence]:
    return session.scalars(select(Expence)).all()


def get_mean(
        session: Session,
) -> int:
    stmt = select(Expence.price).group_by(func.date(Expence.cdate))
    prices = session.scalars(stmt).all()
    return int(sum(prices) / len(prices))
