from typing import Sequence

import sqlalchemy as sa
from sqlalchemy import select
from data.models import Item
from sqlalchemy.orm import Session


def get_list(
        user_id: int,
        session: Session,
) -> Sequence[Item]:
    stmt = select(Item).where(Item.user_id == user_id).order_by(Item.name)
    return session.scalars(stmt).all()


def add_item(
        item_name: str,
        user_id: int,
        session: Session,
) -> Item:

    stmt = select(Item).where(
            sa.and_(
                Item.name == item_name,
                Item.user_id == user_id,
            )
        )
    item = session.scalars(stmt).one_or_none()
    if not item:
        item = Item(
                name=item_name,
                user_id=user_id,
            )
        session.add(item)
        session.commit()
    return item
