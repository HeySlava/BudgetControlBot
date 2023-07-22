import asyncio
import logging

from aiogram import Dispatcher

from handlers import balance
from handlers import base
from handlers import currency
from handlers import items
from handlers import report
from middleware import CurrencyMiddleware
from middleware import DbSessionMiddleware
from mybot import bot
from utils import on_startup


logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
dp.message.middleware(CurrencyMiddleware())
dp.update.outer_middleware(DbSessionMiddleware())


async def main():
    dp.include_router(report.router)
    dp.include_router(items.router)
    dp.include_router(balance.router)
    dp.include_router(currency.router)
    dp.include_router(base.router)
    await on_startup(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
