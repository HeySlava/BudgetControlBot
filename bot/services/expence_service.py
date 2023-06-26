from data.models import Expence
from sqlalchemy.orm import Session


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
