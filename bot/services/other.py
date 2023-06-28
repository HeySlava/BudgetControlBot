from sqlalchemy import Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from data.models import Expence
from data.models import User


def get_report(
        session: Session,
) -> Sequence:
    stmt = select(Expence, User).join(User, User.id == Expence.user_id)
    rows = session.execute(stmt)
    return rows
