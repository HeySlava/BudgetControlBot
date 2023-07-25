import pytest
from sqlalchemy import func
from sqlalchemy import select

from data.models import Item
from services import item_service


@pytest.mark.parametrize(
        'ids,item_name,expected',
        [
            ([0, 0], 'item1', 1),
            ([0, 1], 'item2', 2),
            ([0, 1, 2], 'item3', 3),
        ]
    )
def test_add_item(session, ids, item_name, expected):
    for id_ in ids:
        item_service.add_item(
                item_name=item_name,
                user_id=id_,
                session=session,
            )

    cnt = session.scalar(
            select(func.count(Item.name)).where(Item.name == item_name)
        )
    assert cnt == expected


def test_add_item_one_user(session):
    item_name = 'add_item_test'
    item_service.add_item(
            item_name=item_name,
            user_id=1,
            session=session,
        )

    item_service.add_item(
            item_name=item_name,
            user_id=1,
            session=session,
        )

    cnt = session.scalar(
            select(func.count(Item.name)).where(Item.name == item_name)
        )
    assert cnt == 1
