from typing import List

from sqlalchemy import select
from data.models import Category
from sqlalchemy.orm import Session


def get_list(
        session: Session,
) -> List[Category]:

    stmt = select(Category)
    categories = session.scalars(stmt).all()
    return categories


def add_category(
        category_name: str,
        session: Session,
) -> Category:

    stmt = select(Category).where(Category.name == category_name)
    category = session.scalars(stmt).one_or_none()
    if not category:
        category = Category(
                name=category_name,
            )
        session.add(category)
        session.commit()
    return category
