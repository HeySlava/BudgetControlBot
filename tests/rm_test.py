import pytest
from services import rm_service

from testing.util import fill_in_db
from testing.util import get_random_user


def test_raise_wrong_category(db):
    fill_in_db(session=db, users_number=2, items_number=0)
    user = get_random_user(db)

    with pytest.raises(rm_service.WrongCategoryError):
        rm_service.rm_empty_category(
                user_id=user.id,
                item_name='no such category',
                session=db,
            )


def test_raise_not_empty_category(db):
    fill_in_db(session=db)
    user = get_random_user(db)

    with pytest.raises(rm_service.NotEmptyCategoryError):
        rm_service.rm_empty_category(
                user_id=user.id,
                item_name=user.items[0].name,
                session=db,
            )


def test_success_delete_empty_cat(db):
    fill_in_db(session=db, users_number=10, items_number=1, expenses_number=0)
    user = get_random_user(db)

    retval = rm_service.rm_empty_category(
            user_id=user.id,
            item_name=user.items[0].name,
            session=db,
        )
    assert retval == 0
