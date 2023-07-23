from typing import Sequence
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.models import Item
from config import config


REPORS_CALLBACKS = {
        'Список всех расходов': 'report',
        'Расходы по выбранной категории': 'full_report_by_item',
        f'Последние {config.last} записей': 'last_n',
        'Список расходов за выбранный день': 'custom_day',
        'Группировка по дню': 'by_day',
        'Группировка по категории': 'by_category',
    }


def get_items_kb(
        items: Sequence[Item],
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for c in items:
        kb.button(text=c.name, callback_data=f'item:{c.name}')

    kb.button(text='Добавить тип', callback_data='new_item')
    kb.adjust(1)
    return kb.as_markup()


def reports_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for title, callback in REPORS_CALLBACKS.items():
        kb.button(text=title, callback_data=callback)

    kb.adjust(1)
    return kb.as_markup()


def report_by_item(
        items: Sequence[Item],
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for c in items:
        kb.button(text=c.name, callback_data=f'report:{c.name}')

    kb.adjust(1)
    return kb.as_markup()
