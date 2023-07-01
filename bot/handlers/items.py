import re
from typing import Any

from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup
from aiogram.types import CallbackQuery
from aiogram.types import Message

import keyboards
from mybot import bot
from config import config
from data import db_session
from handlers._responses import RESPONSES
from services import expence_service
from services import item_service


router = Router()


class newExpence(StatesGroup):
    choosing_item = State()
    writing_expence = State()
    writing_item = State()


@router.callback_query(Text(startswith='item'))
async def select_item(cb: CallbackQuery, state: FSMContext):
    # TODO
    if cb.data and cb.message:
        await cb.answer()
        item_name = cb.data.split(':')[-1]
        await state.update_data(chosen_item=item_name)
        await cb.message.answer(RESPONSES['write_expence'])
    await state.set_state(newExpence.writing_expence)


def _is_number(user_response: Any) -> bool:
    pattern = re.compile(r'-?\d+(\.\d+)?\b')
    match = pattern.match(user_response)
    return True if match else False


@router.callback_query(Text('new_item'))
async def add_new_item(callback: CallbackQuery, state: FSMContext):
    if callback.message:
        await callback.message.answer(RESPONSES['write_new_type_name'])
    await callback.answer(show_alert=False)
    await state.set_state(newExpence.writing_item)


@router.message(newExpence.writing_expence)
async def add_expence(m: Message, state: FSMContext):
    session = db_session.create_session()
    user_data = await state.get_data()
    item_name = user_data['chosen_item']

    if not m.text or not m.from_user:
        return

    if not _is_number(m.text):
        return await m.answer(RESPONSES['write_expence'])

    expence_service.add_expence(
            user_id=m.from_user.id,
            item_name=item_name,
            price=m.text,
            session=session,
        )

    for user_id in config.users:
        if m.from_user:
            record = RESPONSES['new_record'].format(
                    text=m.text,
                    item_name=item_name,
                    first_name=m.from_user.first_name,
                )
            await bot.send_message(
                    chat_id=user_id,
                    text=record,
                )

    items = item_service.get_list(session)
    kb = keyboards.get_items_kb(items)
    await m.answer(text=RESPONSES['choose'], reply_markup=kb)

    await state.clear()


@router.message(newExpence.writing_item)
async def writing_new_item(m: Message, state: FSMContext):
    session = db_session.create_session()
    if m.text and m.from_user:
        item_service.add_item(
                item_name=m.text.upper(),
                user_id=m.from_user.id,
                session=session,
            )

        await m.answer(text=RESPONSES['new_item'].format(text=m.text))

    items = item_service.get_list(session)
    kb = keyboards.get_items_kb(items)
    await m.answer(text=RESPONSES['choose'], reply_markup=kb)
    await state.clear()