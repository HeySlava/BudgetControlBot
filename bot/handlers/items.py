from aiogram import Router
from aiogram.filters import Text
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup
from aiogram.types import CallbackQuery
from aiogram.types import Message
from sqlalchemy.orm import Session

import keyboards
import utils
from handlers._responses import RESPONSES
from mybot import bot
from services import expense_service
from services import item_service
from services import user_service


router = Router()


class newExpence(StatesGroup):
    choosing_item = State()
    writing_expence = State()
    writing_item = State()


@router.message(Command('new'))
async def new(message: Message, session: Session):
    items = item_service.get_list(session)
    kb = keyboards.get_items_kb(items)
    await message.answer(
            text=RESPONSES['select_new_type'],
            reply_markup=kb,
        )


@router.callback_query(Text(startswith='item'))
async def select_item(cb: CallbackQuery, state: FSMContext):
    # TODO
    if cb.data and cb.message:
        await cb.answer()
        item_name = cb.data.split(':')[-1]
        await state.update_data(chosen_item=item_name)
        await cb.message.answer(RESPONSES['write_expence'].format(item=item_name))
    await state.set_state(newExpence.writing_expence)


@router.callback_query(Text('new_item'))
async def add_new_item(callback: CallbackQuery, state: FSMContext):
    if callback.message:
        await callback.message.answer(RESPONSES['write_new_type_name'])
    await callback.answer(show_alert=False)
    await state.set_state(newExpence.writing_item)


@router.message(newExpence.writing_expence)
async def add_expense(m: Message, state: FSMContext, session: Session):
    user_data = await state.get_data()
    item_name = user_data['chosen_item']

    if not m.text or not m.from_user:
        return

    user = user_service.get_user_by_id(
            user_id=m.from_user.id,
            session=session,
        )

    users_ids = [user.id]

    cost_string, _, comment = m.text.partition('\n')
    cost_string = cost_string.strip()

    cost = utils.custom_eval(cost_string)
    if cost is None:
        return await m.answer(RESPONSES['write_expence'].format(item=item_name))

    expense_service.add_expense(
            user_id=m.from_user.id,
            item_name=item_name,
            price=cost,
            unit=user.currency,
            comment=comment.strip() if comment else None,
            session=session,
            commit=True,
        )

    for user_id in users_ids:
        if m.from_user:
            record = RESPONSES['new_record'].format(
                    text=cost,
                    item_name=item_name,
                    first_name=m.from_user.first_name,
                )
            if comment and comment.strip():
                comment = comment.strip()
                record += f' со следующими комментариями {comment!r}'

            await bot.send_message(
                    chat_id=user_id,
                    text=record,
                )

    items = item_service.get_list(session)
    kb = keyboards.get_items_kb(items)
    await m.answer(text=RESPONSES['choose'], reply_markup=kb)

    await state.clear()


@router.message(newExpence.writing_item)
async def writing_new_item(m: Message, state: FSMContext, session: Session):
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
