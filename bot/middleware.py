from typing import Callable
from typing import Dict
from typing import Any
from typing import Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.types import Update

from config import config
from data import db_session


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


class DbSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        data['session'] = next(db_session.create_session())
        return await handler(event, data)
