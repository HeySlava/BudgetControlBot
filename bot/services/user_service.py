from typing import Optional
from sqlalchemy import select
from data.models import User
from sqlalchemy.orm import Session


def register_user(
        id: int,
        first_name: str,
        session: Session,
        username: Optional[str] = None,
        last_name: Optional[str] = None,
) -> User:

    stmt = select(User).where(User.id == id)
    user = session.scalars(stmt).one_or_none()
    if not user:
        user = User(
                id=id,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
        session.add(user)
        session.commit()
    return user


def get_user_by_id(
        user_id: int,
        session: Session,
) -> User:
    stmt = select(User).where(User.id == user_id)
    return session.scalars(stmt).one()


def change_balance(
        user: User,
        increment: int,
        session: Session,
        commit: bool = True,
) -> User:
    user.balance += -1 * increment
    session.add(user)
    if commit:
        session.commit()
    return user
