import sqlalchemy as sa
from data.models import Expense
from data.models import Item
from sqlalchemy import select
from sqlalchemy.orm import Session


class WrongCategoryError(ValueError):
    pass


class NotEmptyCategoryError(ValueError):
    pass


def rm_empty_category(
        user_id: int,
        item_name: str,
        session: Session,
) -> int:
    all_items = session.scalars(select(Item.name).where(Item.user_id == user_id))
    if item_name not in all_items:
        raise WrongCategoryError(
            f'No such category {item_name!r} for user {user_id}'
        )

    cnt_stmt = (
            select(Expense.id)
            .where(
                Expense.item_name == item_name,
                Expense.user_id == user_id,
                ~Expense.is_replenishment,
            )
        )
    cnt = len(session.scalars(cnt_stmt).all())

    if cnt > 0:
        raise NotEmptyCategoryError()

    stmt = (
            sa.delete(Item)
            .where(
                Item.user_id == user_id,
                Item.name == item_name,
            )
        )
    session.execute(stmt)
    session.commit()
    return 0
