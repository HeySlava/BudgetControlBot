from typing import List

from sqlalchemy import select
from data.models import Item
from sqlalchemy.orm import Session


def get_list(
        session: Session,
) -> List[Item]:

    return session.scalars(select(Item)).all()


def add_item(
        item_name: str,
        session: Session,
) -> Item:

    stmt = select(Item).where(Item.name == item_name)
    item = session.scalars(stmt).one_or_none()
    if not item:
        item = Item(
                name=item_name,
            )
        session.add(item)
        session.commit()
    return item
