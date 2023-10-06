from logging.config import fileConfig

import data.models  # noqa: F401
import sqlalchemy as sa
from alembic import context
from config import config as settings
from data.models import Base
from sqlalchemy import engine_from_config
from sqlalchemy import pool


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        render_as_batch=True,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    try:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix='sqlalchemy.',
            poolclass=pool.NullPool,
        )
    except KeyError:
        connectable = sa.create_engine(settings.conn_str, echo=False)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
