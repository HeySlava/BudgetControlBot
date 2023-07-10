from pathlib import Path

import pytest
import sqlalchemy as sa
import tempfile
from sqlalchemy.engine import Engine
from sqlalchemy import orm

from data.models import Base
from data.models import User
from data.models import Group
from data.db_session import make_alembic_config


base_dir = Path(__file__).parent.parent / 'bot'


@pytest.fixture(scope='session')
def engine():
    with tempfile.TemporaryDirectory() as dir:
        tmpfile = Path(dir) / 'pytest.db'
        conn_str = f'sqlite:///{tmpfile}'
        engine = sa.create_engine(conn_str)
        yield engine


@pytest.fixture(scope='function')
def db(engine):
    _factory = orm.sessionmaker(engine, expire_on_commit=False)
    session: orm.Session = _factory()
    yield session
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()


@pytest.fixture(scope='function')
def alembic_config(engine: Engine):
    conn_str = str(engine.url)
    config = make_alembic_config(
            conn_str=conn_str,
            migration_script_location=base_dir / 'migrations',
            alembic_config_path=base_dir / 'alembic.ini',
        )
    config.set_main_option('sqlalchemy.url', conn_str)
    return config


@pytest.fixture(scope='session')
def session():
    with tempfile.TemporaryDirectory() as dir:
        tmpfile = Path(dir) / 'money.db'
        conn_str = f'sqlite:///{tmpfile}'
        engine = sa.create_engine(conn_str)
        Base.metadata.create_all(bind=engine)

        _factory = orm.sessionmaker(engine, expire_on_commit=False)
        session: orm.Session = _factory()
        u1 = User(id=1, first_name='test1')
        u2 = User(id=2, first_name='test2')
        u3 = User(id=3, first_name='test3')
        group = Group()
        group.users.extend([u1, u2, u3])
        session.add(group)
        session.commit()

        yield session
