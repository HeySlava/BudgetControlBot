import datetime as dt
import logging
from pathlib import Path
from typing import Optional

from aiogram.types import BotCommand
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy import select
from sqlalchemy.orm import Session

from config import config
from data import db_session
from data.models import Release
from data.models import User
from data.db_session import make_alembic_config


logger = logging.getLogger(__file__)


commands = [
        BotCommand(command='new', description='Команда для работы с расходами'),
        BotCommand(command='report', description='Отчетность по расходам'),
        BotCommand(command='help', description='Показать подсказку'),
        BotCommand(
            command='last',
            description=f'Показать последние {config.last} расходов',
        ),
    ]


def try_datetime(string_dt: str) -> Optional[dt.date]:
    try:
        return dt.datetime.strptime(string_dt, '%Y-%m-%d').date()
    except ValueError:
        return None


async def on_startup(bot):

    Path('./db').mkdir(parents=True, exist_ok=True)
    alembic_config = make_alembic_config(
            conn_str=config.conn_str,
            migration_script_location=config.migration_script_location,
            alembic_config_path=config.alembic_config_path,
        )

    db_session.global_init(
            echo=False,
            config=alembic_config,
        )

    session: Session = next(db_session.create_session())
    stmt = select(Release).where(~Release.is_broadcasted)
    release = session.scalars(stmt).first()
    if release:
        user_ids = session.scalars(select(User.id)).all()
        try:
            for user_id in user_ids:
                try:
                    await bot.send_message(
                            text=release.message,
                            chat_id=user_id,
                        )
                except TelegramBadRequest:
                    logger.exception("Can't send release note to user")
                    pass
        finally:
            release.is_broadcasted = True
            session.add(release)
            session.commit()

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands)
    await bot.send_message(text='Bot has started', chat_id=config.admin)
