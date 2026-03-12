import datetime as dt
from typing import Sequence
from typing import Union

import keyboards
from aiogram import F
from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup
from aiogram.types import CallbackQuery
from aiogram.types import Message
from config import config
from data.models import Expense
from handlers._responses import RESPONSES
from services import expense_service
from services import item_service
from services import report_service
from services import user_service
from sqlalchemy.orm import Session
from utils import try_datetime


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


class Report(StatesGroup):
    writing_date = State()


router = Router()


def _prepare_report_text(expenses: Sequence[Expense], title: str) -> str:
    if not expenses:
        return f'{title}\n\nЗдесь пока пусто.'

    report_lines = [f'{title}\n']
    for expense in expenses:
        cdate_tz_formatted = (
            expense.cdate_tz.strftime('%d.%m %H:%M') if expense.cdate_tz else ''
        )
        txt = (
                f'{expense.user.first_name}  {expense.item_name}  '
                f'{expense.price} {expense.unit}  {cdate_tz_formatted}'
            )
        if expense.comment:
            txt += f'  {expense.comment}'
        report_lines.append(txt.strip())

    return '\n'.join(report_lines)


@router.message(Command('report'))
async def cmd_report(message: Message):
    kb = keyboards.reports_kb()
    await message.answer(
            text='Выбери тип отчета',
            reply_markup=kb,
        )


@router.callback_query(F.data == 'reports_menu')
async def cb_reports_menu(cb: CallbackQuery):
    await cb.answer()
    if not cb.message:
        return
    kb = keyboards.reports_kb()
    await cb.message.edit_text(
            text='Выбери тип отчета',
            reply_markup=kb,
        )


@router.callback_query(F.data == 'last_n')
@router.message(Command('last'))
async def report_last(update: Union[CallbackQuery, Message], session: Session):
    if isinstance(update, CallbackQuery):
        await update.answer()
        m = update.message
    else:
        m = update

    if not m:
        return None

    expenses = expense_service.get_expenses(
            user_id=m.chat.id,
            session=session,
        )

    if len(expenses) > config.last:
        expenses = expenses[-config.last:]

    text = _prepare_report_text(expenses, title=f'Последние {config.last} записей:')
    kb = keyboards.back_button_kb('reports_menu')

    if isinstance(update, CallbackQuery) and update.message:
        await update.message.edit_text(text=text, reply_markup=kb)
    elif m:
        await m.answer(text=text, reply_markup=kb)


@router.callback_query(F.data == 'by_month')
async def group_by_month(cb: CallbackQuery, session: Session):
    await cb.answer()
    if not cb.message:
        return
    user = user_service.get_user_by_id(
            user_id=cb.from_user.id,
            session=session,
        )
    current_month_year = dt.date.today().strftime('%Y-%m')
    total, unit = report_service.get_month_total(
            user=user,
            month_year=current_month_year,
            session=session,
        )
    categories = report_service.get_month_categories(
            user=user,
            month_year=current_month_year,
            session=session,
        )
    title = _month_display_name(current_month_year)
    lines = [f'📅 {title}', f'💰 Всего: {total:,} {unit}']
    text = '\n'.join(lines)
    has_prev, has_next = _has_prev_next(current_month_year, set())
    kb = keyboards.month_categories_kb(
            month_year=current_month_year,
            categories_data=categories,
            has_prev=has_prev,
            has_next=has_next,
        )
    await cb.message.edit_text(text=text, reply_markup=kb)


def _has_prev_next(month_year: str, _months_set: set) -> tuple:
    return (True, True)


@router.callback_query(F.data.startswith('report:month:list'))
async def show_month_list(cb: CallbackQuery, session: Session):
    if not cb.data or not cb.message:
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
    if not cb.data or ':cat:' not in cb.data or not cb.message:
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
            line = f'{e.item_name}  {e.price} {e.unit}  {cdate_tz_formatted}'
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
    if not cb.data or ':nav:' not in cb.data or not cb.message:
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
    user = user_service.get_user_by_id(
            user_id=cb.from_user.id,
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
    lines = [f'📅 {title}', f'💰 Всего: {total:,} {unit}']
    text = '\n'.join(lines)
    kb = keyboards.month_categories_kb(
            month_year=month_year,
            categories_data=categories,
            has_prev=has_prev,
            has_next=has_next,
        )
    await cb.message.edit_text(text=text, reply_markup=kb)


async def show_month_categories(cb: CallbackQuery, session: Session):
    if not cb.data or not cb.message:
        return
    if 'report:month:list' in cb.data or ':nav:' in cb.data or ':cat:' in cb.data:
        return
    parts = cb.data.split(':')
    if len(parts) < 3:
        return
    await cb.answer()
    month_year = parts[2]
    user = user_service.get_user_by_id(
            user_id=cb.from_user.id,
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
    lines = [f'📅 {title}', f'💰 Всего: {total:,} {unit}']
    text = '\n'.join(lines)
    kb = keyboards.month_categories_kb(
            month_year=month_year,
            categories_data=categories,
            has_prev=has_prev,
            has_next=has_next,
        )
    await cb.message.edit_text(text=text, reply_markup=kb)


@router.callback_query(F.data == 'by_category')
async def group_by_category(cb: CallbackQuery, session: Session):
    await cb.answer()

    if not cb.message:
        return

    user = user_service.get_user_by_id(
            user_id=cb.from_user.id,
            session=session,
        )

    rows = report_service.get_report_by_category(
            user=user,
            session=session,
        )

    if not rows:
        text = 'Расходы по категориям:\n\nЗдесь пока пусто.'
    else:
        text = 'Расходы по категориям (за всё время):\n\n' + '\n'.join(rows)

    kb = keyboards.back_button_kb('reports_menu')
    await cb.message.edit_text(text=text, reply_markup=kb)


@router.callback_query(F.data == 'custom_day')
async def group_by_custom_day(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.set_state(Report.writing_date)

    if cb.message and cb.message.from_user:
        await cb.message.answer(RESPONSES['custom_date'])


@router.message(Report.writing_date)
async def report_by_day(m: Message, state: FSMContext, session: Session):
    if not m.text or not m.from_user:
        return

    user_dt = try_datetime(m.text.strip())
    if not user_dt:
        return await m.answer(RESPONSES['custom_date'])

    expenses = expense_service.get_expenses_by_date(
            user_id=m.from_user.id,
            custom_date=user_dt,
            session=session,
        )

    title = f"Записи за {user_dt.strftime('%d.%m.%Y')}:"
    text = _prepare_report_text(expenses, title=title)
    kb = keyboards.back_button_kb('reports_menu')
    await m.answer(text=text, reply_markup=kb)
    await state.clear()


@router.callback_query(F.data == 'full_report_by_item')
async def report_by_items_kb(cb: CallbackQuery, session: Session):
    items = item_service.get_list(cb.from_user.id, session)
    kb = keyboards.report_by_item(items)
    await cb.answer()
    if cb.message:
        await cb.message.answer(
                text='Выбери категорию по которой хочешь получить отчет',
                reply_markup=kb,
            )


@router.callback_query(F.data.startswith('report'))
async def full_report_by_item(cb: CallbackQuery, session: Session):
    await cb.answer()
    if cb.data and cb.message:
        item_name = cb.data.split(':')[-1]
        expenses = expense_service.get_expenses_by_item(
                item_name=item_name,
                user_id=cb.from_user.id,
                session=session,
            )

        title = f'Записи для категории {item_name}:'
        text = _prepare_report_text(expenses, title=title)
        kb = keyboards.back_button_kb('by_category')
        await cb.message.edit_text(text=text, reply_markup=kb)
