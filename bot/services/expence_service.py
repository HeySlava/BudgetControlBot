from data.models import Expence
from sqlalchemy.orm import Session


def add_expence(
        user_id: int,
        category_name: str,
        item_name: str,
        price: int,
        session: Session,
) -> Expence:

    expence = Expence(
            user_id=user_id,
            category_name=category_name,
            item_name=item_name,
            price=price,
        )
    session.add(expence)
    session.commit()
    return expence
