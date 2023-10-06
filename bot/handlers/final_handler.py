from aiogram import Router
from aiogram.types import Message
from handlers.base import HELP_MESSAGE


router = Router()


@router.message()
async def final_handler(message: Message):
    if message.text:
        await message.answer(HELP_MESSAGE, disable_web_page_preview=True)
