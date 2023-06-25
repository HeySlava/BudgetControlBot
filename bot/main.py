import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters.command import Command

from config import config

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.token.get_secret_value())
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('Hello!')


async def cmd_test2(message: Message):
    await message.reply('Test 2')


@dp.message(Command('show_list'))
async def cmd_show_list(message: Message, mylist: list[int]):
    await message.answer(f'Ваш список: {mylist}')


async def main():
    dp.message.register(cmd_test2, Command('test2'))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, mylist=[1, 2, 3])


if __name__ == '__main__':
    asyncio.run(main())
