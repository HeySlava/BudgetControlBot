from typing import Sequence
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.models import Item


def get_items_kb(
        items: Sequence[Item],
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for c in items:
        kb.button(text=c.name, callback_data=f'item:{c.name}')

    kb.button(text='Добавить тип', callback_data='new_item')
    kb.adjust(1)
    return kb.as_markup()
