from typing import Sequence

import sqlalchemy as sa
from sqlalchemy import select
from data.models import Item
from sqlalchemy.orm import Session


def get_list(
        category_name: str,
        session: Session,
) -> Sequence[Item]:
    stmt = select(Item).where(Item.category_name == category_name)
    return session.scalars(stmt).all()


def add_item(
        item_name: str,
        category_name: str,
        session: Session,
) -> Item:

    stmt = select(Item).where(
            sa.and_(
                Item.name == item_name,
                Item.category_name == category_name,
            )
        )
    item = session.scalars(stmt).one_or_none()
    if not item:
        item = Item(
                name=item_name,
                category_name=category_name,
            )
        session.add(item)
        session.commit()
    return item
