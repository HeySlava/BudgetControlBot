import pytest
from sqlalchemy.orm import Session
from sqlalchemy import func

from data.models import User
from services import group_service


def test_group_members(session: Session):
    assert 7 == session.scalar(func.count(User.id))


@pytest.mark.parametrize(
        'group_id,expected_ids',
        [
            (1, [0, 1, 2, 3]),
            (2, [4, 5, 6]),
        ],
    )
def test_members_list(session: Session, group_id, expected_ids):
    group = group_service.get_group_by_id(group_id=group_id, session=session)
    assert sorted([u.id for u in group.users]) == expected_ids


def test_not_group(session: Session):
    group = group_service.get_group_by_id(group_id=-1, session=session)
    assert group is None
