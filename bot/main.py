import asyncio
import logging
from pathlib import Path

from aiogram import Dispatcher
from aiogram import Router
from aiogram.types import BotCommand

from mybot import bot
from config import config
from data import db_session
from data.db_session import make_alembic_config
from handlers import base
from handlers import items
from handlers import report
from middleware import AuthentificationMiddleware


router = Router()
router.message.outer_middleware(AuthentificationMiddleware())

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()


commands = [
        BotCommand(command='start', description='Начать работать с ботом'),
        BotCommand(command='new', description='Команда для работы с расходами'),
        BotCommand(command='report', description='Отчетность по расходам'),
        BotCommand(command='help', description='Показать подсказку'),
    ]


async def main():
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

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands)
    dp.include_router(router)
    dp.include_router(report.router)
    dp.include_router(items.router)
    dp.include_router(base.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
