import sqlalchemy as sa
from sqlalchemy import orm

from data import models  # noqa: F401
from data.models import Base


_factory = None


def global_init(
        conn_str: str,
        echo: bool,
) -> None:
    global _factory

    if _factory:
        return

    if not conn_str or not conn_str.strip():
        raise Exception('You have to specify conn_str, but your {!r:conn_str}')

    engine = sa.create_engine(
            conn_str,
            echo=echo,
            connect_args={'check_same_thread': False},
        )

    Base.metadata.create_all(bind=engine)

    _factory = orm.sessionmaker(bind=engine)


def create_session():
    global _factory

    if not _factory:
        raise Exception('You must call global_init() before using this method')

    session: orm.Session = _factory()

    try:
        return session
    finally:
        session.close()
