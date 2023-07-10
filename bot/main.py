import asyncio
import logging

from aiogram import Dispatcher

from handlers import base
from handlers import items
from handlers import report
from middleware import AuthentificationMiddleware
from middleware import DbSessionMiddleware
from mybot import bot
from utils import on_startup


logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
dp.message.outer_middleware(AuthentificationMiddleware())
dp.update.outer_middleware(DbSessionMiddleware())


async def main():
    dp.include_router(report.router)
    dp.include_router(items.router)
    dp.include_router(base.router)
    await on_startup(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
