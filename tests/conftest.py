from pathlib import Path

import pytest
import sqlalchemy as sa
import tempfile
from sqlalchemy.engine import Engine
from sqlalchemy import orm

from data.models import Base
from data.models import Expense
from data.models import Group
from data.models import Item
from data.models import User
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


@pytest.fixture(scope='function')
def session():
    with tempfile.TemporaryDirectory() as dir:
        tmpfile = Path(dir) / 'money.db'
        conn_str = f'sqlite:///{tmpfile}'
        engine = sa.create_engine(conn_str)
        Base.metadata.create_all(bind=engine)

        _factory = orm.sessionmaker(engine, expire_on_commit=False)
        session: orm.Session = _factory()
        group1 = Group()
        item_name = 'Test'
        user = User(id=0, first_name='test0')
        item = Item(name=item_name)
        user.items.append(item)
        group1.users.append(user)

        for i in range(1, 4):
            user = User(id=i, first_name=f'test{i}')
            group1.users.append(user)
            for _ in range(1, 3):
                expense = Expense(item_name=item_name, price=100, group_id=group1.id)
                user.expenses.append(expense)

        group2 = Group()
        for i in range(4, 7):
            user = User(id=i, first_name=f'test{i}')
            group2.users.append(User(id=i, first_name=f'test{i}'))
            for _ in range(1, 3):
                expense = Expense(item_name=item_name, price=100, group_id=group2.id)
                user.expenses.append(expense)

        session.add_all([group1, group2])
        session.commit()

        yield session
