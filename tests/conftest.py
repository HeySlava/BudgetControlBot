import tempfile
from pathlib import Path

import pytest
import sqlalchemy as sa
from data.db_session import make_alembic_config
from data.models import Base
from data.models import Expense
from data.models import Item
from data.models import User
from sqlalchemy import orm
from sqlalchemy.engine import Engine


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
        item_name = 'Test'
        user = User(id=0, first_name='test0')
        item = Item(name=item_name)
        user.items.append(item)

        for i in range(1, 4):
            user = User(id=i, first_name=f'test{i}')
            for _ in range(1, 3):
                for unit in 'unit1', 'unit2':
                    expense = Expense(item_name=item_name, price=100, unit=unit)
                    user.expenses.append(expense)
            session.add(user)

        session.commit()

        yield session
