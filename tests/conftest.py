import tempfile
from pathlib import Path

import pytest
import sqlalchemy as sa
from data.db_session import make_alembic_config
from data.models import Base
from sqlalchemy import orm
from sqlalchemy.engine import Engine

from testing.util import base_dir


@pytest.fixture(scope='function')
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
    Base.metadata.create_all(bind=engine)

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
