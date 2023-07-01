import asyncio
import logging
import re
from pathlib import Path
from typing import Any

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import Router
from aiogram.filters import Text
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup
from aiogram.types import BotCommand
from aiogram.types import CallbackQuery
from aiogram.types import Message

import keyboards
from config import config
from data import db_session
from data.db_session import make_alembic_config
from handlers import base
from handlers import report
from middleware import AuthentificationMiddleware
from services import expence_service
from services import item_service


router = Router()
router.message.outer_middleware(AuthentificationMiddleware())

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.token)
dp = Dispatcher()


class newExpence(StatesGroup):
    choosing_item = State()
    writing_expence = State()
    writing_item = State()


commands = [
        BotCommand(command='start', description='Начать работать с ботом'),
        BotCommand(command='new', description='Команда для работы с расходами'),
        BotCommand(command='report', description='Отчетность по расходам'),
        BotCommand(command='help', description='Показать подсказку'),
    ]


RESPONSES = {
        'write_expence': 'Впиши свой расход, это должно быть число',
        'new_record': (
            'Пользователь {first_name} добавил новую запись для категории '
            '{item_name!r} на сумму {text} AMD'
        ),
        'new_item': 'Расход {text!r} доступен в общем списке',
        'choose': 'Выбирай',
        'select_new_type': 'Выбери тип расхода',
        'write_new_type_name': 'Напиши название для нового типа расходов',
    }


def _is_number(user_response: Any) -> bool:
    pattern = re.compile(r'-?\d+(\.\d+)?\b')
    match = pattern.match(user_response)
    return True if match else False


@router.message(Command('new'))
async def new(message: Message):
    session = db_session.create_session()
    items = item_service.get_list(session)
    kb = keyboards.get_items_kb(items)
    await message.answer(
            text=RESPONSES['select_new_type'],
            reply_markup=kb,
        )


@router.callback_query(Text('new_item'))
async def add_new_item(callback: CallbackQuery, state: FSMContext):
    if callback.message:
        await callback.message.answer(RESPONSES['write_new_type_name'])
    await callback.answer(show_alert=False)
    await state.set_state(newExpence.writing_item)


@router.callback_query(Text(startswith='item'))
async def select_item(cb: CallbackQuery, state: FSMContext):
    # TODO
    if cb.data:
        item_name = cb.data.split(':')[-1]
        await state.update_data(chosen_item=item_name)
        await state.set_state(newExpence.writing_expence)
        await cb.answer()

    if cb.message:
        await cb.answer()
        await cb.message.answer(RESPONSES['write_expence'])


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


async def main():
    Path('./db').mkdir(parents=True, exist_ok=True)
    alembic_config = make_alembic_config(
            conn_str=config.conn_str,
            migration_script_location=config.migration_script_location,
            alembic_config_path=config.alembic_config_path,
        )

    db_session.global_init(
            echo=False,
            config=alembic_config,
        )

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands)
    dp.include_router(router)
    dp.include_router(report.router)
    dp.include_router(base.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
