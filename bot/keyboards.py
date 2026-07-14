from typing import Sequence
from typing import Tuple

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def _month_display(month_year: str, total: int, unit: str) -> str:
    y, m = month_year[:4], int(month_year[5:7])
    months_ru = (
        'Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
        'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек',
    )
    return f'{months_ru[m - 1]} {y} — {total:,} {unit}'


def get_items_kb(
        items: Sequence,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for c in items:
        kb.button(text=c.name, callback_data=f'item:{c.name}')

    kb.button(text='Добавить тип', callback_data='new_item')
    kb.adjust(1)
    return kb.as_markup()


def month_list_kb(
        months_data: Sequence[Tuple[str, int, str]],
        page: int = 0,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    page_size = 12
    start = page * page_size
    end = start + page_size
    slice_ = months_data[start:end]

    for month_year, total, unit in slice_:
        text = _month_display(month_year, total, unit)
        kb.button(text=text, callback_data=f'report:month:{month_year}')

    total_pages = (len(months_data) + page_size - 1) // page_size
    if total_pages > 1:
        if page > 0:
            kb.button(
                text='<<',
                callback_data=f'report:month:list:{page - 1}',
            )
        if page < total_pages - 1:
            kb.button(
                text='>>',
                callback_data=f'report:month:list:{page + 1}',
            )

    if total_pages > 1:
        kb.adjust(*([1] * len(slice_)), 2 if page and page < total_pages - 1 else 1)
    else:
        kb.adjust(*([1] * len(slice_)))
    return kb.as_markup()


def month_categories_kb(
        month_year: str,
        categories_data: Sequence[Tuple[str, int, str]],
        has_prev: bool,
        has_next: bool,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for i, (item_name, total, unit) in enumerate(categories_data):
        text = f'{item_name} — {total:,} {unit}'
        kb.button(text=text, callback_data=f'report:month:{month_year}:cat:{i}')
    if has_prev:
        kb.button(text='<<', callback_data=f'report:month:{month_year}:nav:prev')
    kb.button(text='Выбрать месяц', callback_data='report:month:list:0')
    if has_next:
        kb.button(text='>>', callback_data=f'report:month:{month_year}:nav:next')
    kb.button(text='Назад', callback_data='report:month:list')
    n_cat = len(categories_data)
    kb.adjust(*([1] * n_cat), 3, 1)
    return kb.as_markup()


def back_button_kb(back_callback: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Назад', callback_data=back_callback)
    return kb.as_markup()
