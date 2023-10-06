from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.types import Update
from config import config
from data import db_session
from services import user_service
from sqlalchemy.exc import NoResultFound


class AuthentificationMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.from_user and event.from_user.id in [config.admin]:
            return await handler(event, data)

        await event.answer(
            text='Бот находится в разработке',
        )


class CurrencyMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        session = next(db_session.create_session())
        if event.from_user and event.from_user.id:
            try:
                user = user_service.get_user_by_id(event.from_user.id, session)
            except NoResultFound:
                return await handler(event, data)

            if event.text and event.text.startswith('/currency'):
                return await handler(event, data)

            if not user.currency:
                await event.answer(
                        text=(
                            'Для начала работы с ботом необходимо установить валюту. '
                            'Установи валюту командой:\n\n/currency ВАЛЮТА'
                        )
                    )
            else:
                return await handler(event, data)


class DbSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        data['session'] = next(db_session.create_session())
        return await handler(event, data)
