from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from sqlalchemy.orm import Session

from services import user_service


router = Router()


HELP_MESSAGE = (
        'Для работы с расходами - /new'
        '\n'
        'Для отображения истории - /report'
        '\n'
        '\n'
        'Посмотреть текущую валюту - /currency'
        '\n'
        'Изменить валюту - /currency ВАЛЮТА'
        '\n'
        '\n'
        'Посмотреть баланс - /balance или /b'
        '\n'
        'Изменить баланс на число - /balance ЧИСЛО'
        '\n'
        '\n'
        'Увидеть это сообщение - /help'
    )


@router.message(Command('start'))
async def cmd_start(message: Message, session: Session):
    if message.from_user:
        user_service.register_user(
                id=message.from_user.id,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                username=message.from_user.username,
                session=session,
            )
    await message.answer(HELP_MESSAGE)


@router.message(Command('help'))
async def cmd_help(message: Message):
    if message.from_user:
        await message.answer(HELP_MESSAGE)


@router.message()
async def final_handler(message: Message):
    if message.text:
        await message.answer(HELP_MESSAGE)
