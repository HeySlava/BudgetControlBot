from typing import List
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.models import Category


def get_category_kb(
        categories: List[Category]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for c in categories:
        kb.button(text=c.name, callback_data=c.name)

    kb.button(text='Добавить категорию', callback_data='new_category')
    kb.adjust(1)
    return kb.as_markup()


def get_items_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Добавить тип', callback_data='new_item')
    return kb.as_markup()
