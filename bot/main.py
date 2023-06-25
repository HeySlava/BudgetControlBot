import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters.command import Command

from config import config
from data import db_session
from services import user_service

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.token.get_secret_value())
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: Message):
    session = db_session.create_session()
    if message.from_user:
        user = user_service.register_user(
                id=message.from_user.id,
                first_name=message.from_user.first_name,
                session=session,
            )
        print(user)

    await message.answer('Hello!')


async def echo(message: Message):
    if message.text:
        await message.answer(message.text)


async def main():
    db_session.global_init(
            echo=True,
            conn_str='sqlite://',
        )
    dp.message.register(echo)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
