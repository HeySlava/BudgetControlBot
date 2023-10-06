from aiogram import Router
from aiogram.filters import CommandObject
from aiogram.filters.command import Command
from aiogram.types import Message
from services import user_service
from sqlalchemy.orm import Session


router = Router()


@router.message(Command('currency'))
async def balance(message: Message, session: Session, command: CommandObject):
    user = user_service.get_user_by_id(message.chat.id, session)
    currency = user.currency
    if command.args:
        currency = command.args.strip()
        user.currency = currency
        session.add(user)
        session.commit()

    text = 'Изменить валюту - /currency ВАЛЮТА\n\n'
    text += f'Текущая валюта {currency!r}'
    await message.answer(text)
