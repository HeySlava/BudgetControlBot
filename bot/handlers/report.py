from typing import List
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

import keyboards
from data import db_session
from data.models import Expense
from data.models import Item
from data.models import User
from handlers._responses import RESPONSES
from services import expense_service
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
async def full_report(cb: CallbackQuery):
    session = db_session.create_session()
    expenses = expense_service.get_expenses(session)
    await cb.answer()
    if not cb.message:
        return
    for msg in _prepare_report(expenses):
        await cb.message.answer(msg)


@router.callback_query(Text('last_15'))
async def report_last(cb: CallbackQuery):
    session = db_session.create_session()
    expenses = expense_service.get_expenses(session)
    await cb.answer()
    if not cb.message:
        return
    if len(expenses) > 15:
        expenses = expenses[-15:]
    for msg in _prepare_report(expenses):
        await cb.message.answer(msg)


@router.callback_query(Text('mean'))
async def mean(cb: CallbackQuery):
    session = db_session.create_session()
    mean = expense_service.get_mean(session)
    await cb.answer()
    if cb.message:
        await cb.message.answer(f'Средний расход {mean} драм')


@router.callback_query(Text('by_user'))
async def group_by_user(cb: CallbackQuery):
    session = db_session.create_session()
    await cb.answer()
    rows = other.get_report_by(
            session,
            group_by=User.first_name,
        )
    for msg in _chunkineze(rows, chunk_size=50):
        if cb.message:
            await cb.message.answer(msg)


@router.callback_query(Text('by_day'))
async def group_by_day(cb: CallbackQuery):
    session = db_session.create_session()
    await cb.answer()
    rows = other.get_report_by(
            session,
            group_by=func.date(Expense.cdate_tz),
        )
    for msg in _chunkineze(rows, chunk_size=50):
        if cb.message:
            await cb.message.answer(msg)


@router.callback_query(Text('by_category'))
async def group_by_category(cb: CallbackQuery):
    session = db_session.create_session()
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
async def report_by_day(m: Message, state: FSMContext):
    session = db_session.create_session()
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
