from typing import Callable
from typing import Dict
from typing import Any
from typing import Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from config import config


class AuthentificationMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.from_user and event.from_user.id in config.users:
            return await handler(event, data)

        await event.answer(
            text='Бот находится в разработке',
        )
