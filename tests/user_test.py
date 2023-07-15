import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session
from services import user_service

from data.models import User


def test_default_balance(session: Session):
    user = session.scalars(select(User).where(User.id == 0)).first()
    assert user and user.balance == 0


@pytest.mark.parametrize('increment', [10, -10])
def test_change_balance(session: Session, increment):
    user = session.scalars(select(User).where(User.id == 0)).first()
    user = user_service.change_balance(user, increment, session)
    assert user.balance == increment
