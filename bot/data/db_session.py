import logging
from pathlib import Path

from alembic.config import Config
from alembic import command
import sqlalchemy as sa
from sqlalchemy import orm

from data import models  # noqa: F401


logger = logging.getLogger(__name__)
_factory = None


def make_alembic_config(
        conn_str: str,
        alembic_config_path: Path,
        migration_script_location: Path,
) -> Config:

    config = Config(
            file_=alembic_config_path,
        )

    config.set_main_option('sqlalchemy.url', conn_str)
    config.set_main_option('script_location', migration_script_location.as_posix())

    return config


def global_init(
        config: Config,
        echo: bool,
) -> None:
    global _factory

    if _factory:
        return None

    conn_str = config.get_main_option('sqlalchemy.url')
    if not conn_str:
        raise Exception('You must specify conn_str')

    engine = sa.create_engine(
            conn_str,
            echo=echo,
            pool_size=50,
            max_overflow=70,
        )
    _factory = orm.sessionmaker(engine, expire_on_commit=False)

    with engine.begin() as connection:
        config.attributes['connection'] = connection
        config.attributes['configure_logger'] = False
        command.upgrade(config, 'head')


def count_function_calls(func):
    cnt = 1

    def wrapper(*args, **kwargs):
        nonlocal cnt
        func.cnt = cnt
        cnt += 1
        logger.info(f'Enter function {func.__name__!r} with number {func.cnt!r}')
        result = func(*args, **kwargs)
        logger.info(f'Exit function with {func.__name__!r} with number {func.cnt!r}')
        return result
    return wrapper


@count_function_calls
def create_session():
    global _factory

    if not _factory:
        raise Exception('You must call global_init() before using this method')

    session: orm.Session = _factory()

    try:
        yield session
    finally:
        session.close()
