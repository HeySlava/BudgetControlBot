import pytest
from data.models import Item
from services import item_service
from sqlalchemy import func
from sqlalchemy import select

from testing.util import fill_in_db


@pytest.mark.parametrize(
        'ids,item_name,expected',
        [
            ([0, 0], 'item1', 1),
            ([0, 1], 'item2', 2),
            ([0, 1, 2], 'item3', 3),
        ]
    )
def test_add_item(db, ids, item_name, expected):
    fill_in_db(session=db, users_number=3, currencies=['unit1', 'unit2'])

    for id_ in ids:
        item_service.add_item(
                item_name=item_name,
                user_id=id_,
                session=db,
            )

    cnt = db.scalar(
            select(func.count(Item.name)).where(Item.name == item_name)
        )
    assert cnt == expected


def test_add_item_one_user(db):
    item_name = 'add_item_test'
    item_service.add_item(
            item_name=item_name,
            user_id=1,
            session=db,
        )

    item_service.add_item(
            item_name=item_name,
            user_id=1,
            session=db,
        )

    cnt = db.scalar(
            select(func.count(Item.name)).where(Item.name == item_name)
        )
    assert cnt == 1
