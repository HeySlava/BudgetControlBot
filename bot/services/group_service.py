from typing import Optional

from sqlalchemy.orm import Session

from data.models import Group
from sqlalchemy import select


def get_group_by_id(
        group_id: int,
        session: Session,
) -> Optional[Group]:
    return session.scalars(select(Group).where(Group.id == group_id)).one_or_none()
