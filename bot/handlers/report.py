import datetime as dt

import keyboards
from aiogram import F
from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery
from aiogram.types import Message
from services import report_service
from services import user_service
from sqlalchemy.orm import Session


def _month_year_add(month_year: str, delta_months: int) -> str:
    y, m = int(month_year[:4]), int(month_year[5:7])
    total = (y - 1) * 12 + (m - 1) + delta_months
    ny = total // 12 + 1
    nm = total % 12 + 1
    return dt.date(ny, nm, 1).strftime('%Y-%m')


def _month_display_name(month_year: str) -> str:
    y, m = month_year[:4], int(month_year[5:7])
    months_ru = (
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь',
    )
    return f'{months_ru[m - 1]} {y}'


def _has_prev_next(month_year: str, _months_set: set) -> tuple:
    return (True, True)


router = Router()


async def _show_month(
        target: Message | CallbackQuery,
        user_id: int,
        month_year: str,
        session: Session,
) -> None:
    user = user_service.get_user_by_id(
            user_id=user_id,
            session=session,
        )
    months_data = report_service.get_months_summary(user=user, session=session)
    months_set = {m[0] for m in months_data}
    has_prev, has_next = _has_prev_next(month_year, months_set)
    total, unit = report_service.get_month_total(
            user=user,
            month_year=month_year,
            session=session,
        )
    categories = report_service.get_month_categories(
            user=user,
            month_year=month_year,
            session=session,
        )
    title = _month_display_name(month_year)
    text = '\n'.join([f'📅 {title}', f'💰 Всего: {total:,} {unit}'])
    kb = keyboards.month_categories_kb(
            month_year=month_year,
            categories_data=categories,
            has_prev=has_prev,
            has_next=has_next,
        )

    if isinstance(target, CallbackQuery) and target.message:
        await target.message.edit_text(text=text, reply_markup=kb)
    elif isinstance(target, Message):
        await target.answer(text=text, reply_markup=kb)


@router.message(Command('report'))
async def cmd_report(message: Message, session: Session):
    current_month_year = dt.date.today().strftime('%Y-%m')
    await _show_month(
            target=message,
            user_id=message.chat.id,
            month_year=current_month_year,
            session=session,
        )


@router.callback_query(F.data.startswith('report:month:list'))
async def show_month_list(cb: CallbackQuery, session: Session):
    if not cb.data or not cb.message or not cb.from_user:
        return
    await cb.answer()
    user = user_service.get_user_by_id(
            user_id=cb.from_user.id,
            session=session,
        )
    months_data = report_service.get_months_summary(user=user, session=session)
    if not months_data:
        await cb.message.edit_text(text='Нет данных за периоды.', reply_markup=None)
        return

    parts = cb.data.split(':')
    page = 0
    if len(parts) >= 4:
        try:
            page = int(parts[3])
        except ValueError:
            page = 0

    kb = keyboards.month_list_kb(months_data, page=page)
    await cb.message.edit_text(text='Выбери месяц', reply_markup=kb)


@router.callback_query(F.data.startswith('report:month:'))
async def dispatch_month_callbacks(cb: CallbackQuery, session: Session):
    if not cb.data:
        return
    if ':cat:' in cb.data:
        return await show_category_details(cb, session)
    if ':nav:' in cb.data:
        return await navigate_month(cb, session)
    if 'report:month:list' not in cb.data:
        return await show_month_categories(cb, session)


async def show_category_details(cb: CallbackQuery, session: Session):
    if not cb.data or ':cat:' not in cb.data or not cb.message or not cb.from_user:
        return
    await cb.answer()
    parts = cb.data.split(':')
    if len(parts) < 5:
        return
    month_year = parts[2]
    try:
        cat_index = int(parts[-1])
    except ValueError:
        return
    user = user_service.get_user_by_id(
            user_id=cb.from_user.id,
            session=session,
        )
    categories = report_service.get_month_categories(
            user=user,
            month_year=month_year,
            session=session,
        )
    if cat_index < 0 or cat_index >= len(categories):
        return
    item_name = categories[cat_index][0]
    by_day = report_service.get_category_by_day(
            user=user,
            month_year=month_year,
            item_name=item_name,
            session=session,
        )
    expenses = report_service.get_category_details(
            user=user,
            month_year=month_year,
            item_name=item_name,
            session=session,
        )
    if len(expenses) <= 10:
        report_lines = []
        for e in expenses:
            cdate_tz_formatted = (
                e.cdate_tz.strftime('%d.%m %H:%M') if e.cdate_tz else ''
            )
            line = f'{e.price} {e.unit}  {cdate_tz_formatted}'
            if e.comment:
                line += f'  {e.comment}'
            report_lines.append(line)
        text = '\n'.join(report_lines)
    else:
        lines = [f'{d}  |  {t:,} {u}' for d, t, u in by_day]
        text = '\n'.join(lines)
    kb = keyboards.back_button_kb(f'report:month:{month_year}')
    await cb.message.edit_text(text=text or 'Нет записей', reply_markup=kb)


async def navigate_month(cb: CallbackQuery, session: Session):
    if not cb.data or ':nav:' not in cb.data or not cb.message or not cb.from_user:
        return
    await cb.answer()
    parts = cb.data.split(':')
    if len(parts) < 4:
        return
    month_year = parts[2]
    nav_part = cb.data.split(':nav:')[-1]
    if nav_part == 'prev':
        month_year = _month_year_add(month_year, -1)
    elif nav_part == 'next':
        month_year = _month_year_add(month_year, 1)
    elif nav_part.startswith('jump:'):
        delta = int(nav_part.split(':')[1])
        month_year = _month_year_add(month_year, delta)
    else:
        return
    await _show_month(
            target=cb,
            user_id=cb.from_user.id,
            month_year=month_year,
            session=session,
        )


async def show_month_categories(cb: CallbackQuery, session: Session):
    if not cb.data or not cb.message or not cb.from_user:
        return
    if 'report:month:list' in cb.data or ':nav:' in cb.data or ':cat:' in cb.data:
        return
    parts = cb.data.split(':')
    if len(parts) < 3:
        return
    await cb.answer()
    month_year = parts[2]
    await _show_month(
            target=cb,
            user_id=cb.from_user.id,
            month_year=month_year,
            session=session,
        )
