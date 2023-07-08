from typing import List, Union
from typing import Sequence

import pytz
from aiogram import Router
from aiogram.filters import Text
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup
from aiogram.types import CallbackQuery
from aiogram.types import Message
from sqlalchemy import func
from sqlalchemy.orm import Session

import keyboards
from config import config
from data.models import Expense
from data.models import Item
from data.models import User
from handlers._responses import RESPONSES
from services import expense_service
from services import item_service
from services import other
from utils import try_datetime


class Report(StatesGroup):
    writing_date = State()


router = Router()

tz = pytz.timezone('Asia/Yerevan')


def _prepare_report(expenses: Sequence[Expense]) -> List[str]:
    report_lines = []
    for expense in expenses:
        cdate_tz_formatted = expense.cdate_tz.strftime('%d.%m %H:%M')
        txt = (
                f'{expense.user.first_name}  {expense.item_name}  '
                f'{expense.price }  {cdate_tz_formatted}'
            )
        if expense.comment:
            txt += f'  {expense.comment}'
        report_lines.append(txt.strip())

    return _chunkineze(report_lines, chunk_size=50)


def _chunkineze(input_array: List[str], chunk_size: int = 50) -> List[str]:
    chunks = [
            input_array[i:i+chunk_size]
            for i in range(0, len(input_array), chunk_size)
        ]
    return ['\n'.join(chunk) for chunk in chunks]


@router.message(Command('report'))
async def cmd_report(message: Message):
    kb = keyboards.reports_kb()
    await message.answer(
            text='Выбери тип отчета',
            reply_markup=kb,
        )


@router.callback_query(Text('report'))
async def full_report(cb: CallbackQuery, session: Session):
    expenses = expense_service.get_expenses(session)
    await cb.answer()
    if not cb.message:
        return
    for msg in _prepare_report(expenses):
        await cb.message.answer(msg)


@router.callback_query(Text('last_n'))
@router.message(Command('last'))
async def report_last(update: Union[CallbackQuery, Message], session: Session):
    expenses = expense_service.get_expenses(session)
    if isinstance(update, CallbackQuery):
        await update.answer()
        m = update.message
    else:
        m = update

    if not m:
        return None

    if len(expenses) > config.last:
        expenses = expenses[-config.last:]
    for msg in _prepare_report(expenses):
        await m.answer(msg)


@router.callback_query(Text('mean'))
async def mean(cb: CallbackQuery, session: Session):
    mean = expense_service.get_mean(session)
    await cb.answer()
    if cb.message:
        await cb.message.answer(f'Средний расход {mean} драм')


@router.callback_query(Text('by_user'))
async def group_by_user(cb: CallbackQuery, session: Session):
    await cb.answer()
    rows = other.get_report_by(
            session,
            group_by=User.first_name,
        )
    for msg in _chunkineze(rows, chunk_size=50):
        if cb.message:
            await cb.message.answer(msg)


@router.callback_query(Text('by_day'))
async def group_by_day(cb: CallbackQuery, session: Session):
    await cb.answer()
    rows = other.get_report_by(
            session,
            group_by=func.date(Expense.cdate_tz),
        )
    for msg in _chunkineze(rows, chunk_size=50):
        if cb.message:
            await cb.message.answer(msg)


@router.callback_query(Text('by_category'))
async def group_by_category(cb: CallbackQuery, session: Session):
    await cb.answer()
    rows = other.get_report_by(
            session,
            group_by=Item.name,
        )
    for msg in _chunkineze(rows, chunk_size=50):
        if cb.message:
            await cb.message.answer(msg)


@router.callback_query(Text('custom_day'))
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
            custom_date=user_dt,
            session=session,
        )

    for msg in _prepare_report(expenses):
        await m.answer(msg)
    await state.clear()


@router.callback_query(Text('full_report_by_item'))
async def report_by_items_kb(cb: CallbackQuery, session: Session):
    items = item_service.get_list(session)
    kb = keyboards.report_by_item(items)
    await cb.answer()
    if cb.message:
        await cb.message.answer(
                text='Выбери категорию по которой хочешь получить отчет',
                reply_markup=kb,
            )


@router.callback_query(Text(startswith='report'))
async def full_report_by_item(cb: CallbackQuery, session: Session):
    await cb.answer()
    if cb.data and cb.message:
        item_name = cb.data.split(':')[-1]
        expenses = expense_service.get_expenses_by_item(item_name, session)

        for msg in _prepare_report(expenses):
            await cb.message.answer(msg)
