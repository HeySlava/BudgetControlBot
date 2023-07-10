from sqlalchemy.orm import Session
from sqlalchemy import func

from data.models import User
from services import group_service


def test_group_members(session: Session):
    assert 3 == session.scalar(func.count(User.id))


def test_members_list(session: Session):
    group = group_service.get_group_by_id(group_id=1, session=session)
    assert sorted([u.id for u in group.users]) == [1, 2, 3]


def test_not_group(session: Session):
    group = group_service.get_group_by_id(group_id=-1, session=session)
    assert group is None
