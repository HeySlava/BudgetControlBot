import asyncio
import logging
from pathlib import Path

from aiogram import Router
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.types import BotCommand, Message
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup
from aiogram.fsm.state import State
from aiogram.filters.command import Command
from aiogram.filters import Text

import keyboards
from config import config
from data import db_session
from services import user_service
from services import item_service
from services import expence_service
from middleware import AuthentificationMiddleware


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
    ]


@router.message(Command('start'))
async def cmd_start(message: Message):
    session = db_session.create_session()
    if message.from_user:
        user_service.register_user(
                id=message.from_user.id,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                username=message.from_user.username,
                session=session,
            )

    await message.answer('Для работы с ботом используй команду /new')


@router.message(Command('new'))
async def new(message: Message):
    session = db_session.create_session()
    items = item_service.get_list(session)
    kb = keyboards.get_items_kb(items)
    await message.answer(
            text='Выбери тип расхода',
            reply_markup=kb,
        )


@router.callback_query(Text('new_item'))
async def add_new_item(callback: CallbackQuery, state: FSMContext):
    if callback.message:
        await callback.message.answer('Теперь напиши название нового товара')
    await callback.answer(
        show_alert=False,
    )
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
        await cb.message.answer(
                'Впиши свой расход, это должно быть число. '
                'Это должно быть число, пока что никакой валидации нет'
            )


@router.message(newExpence.writing_expence)
async def add_expence(m: Message, state: FSMContext):
    session = db_session.create_session()
    user_data = await state.get_data()
    item_name = user_data['chosen_item']
    if m.text and m.from_user:
        expence_service.add_expence(
                user_id=m.from_user.id,
                item_name=item_name,
                price=m.text,
                session=session,
            )

    items = item_service.get_list(session)
    kb = keyboards.get_items_kb(items)

    await m.answer('Запись добавлена в расходы')
    await m.answer(text='Выбирай', reply_markup=kb)
    for user_id in config.users:
        if m.from_user and m.from_user.id != user_id:
            await bot.send_message(
                    chat_id=user_id,
                    text=(
                        f'Добавлен новый расход для категории {item_name} на сумму '
                        f'{m.text} драм'
                    )
                )

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

        await m.answer(
                text=f'Добавлена новая позиция {m.text!r}',
        )

    items = item_service.get_list(session)
    kb = keyboards.get_items_kb(items)
    await m.answer(text='Выбирай', reply_markup=kb)
    await state.clear()


@router.callback_query()
async def echo_callback(callback: CallbackQuery):
    await callback.answer(
        text='Спасибо, что воспользовались ботом!',
        show_alert=False,
    )


async def echo(message: Message):
    if message.text:
        await message.answer(message.text)


async def main():
    Path('./db').mkdir(parents=True, exist_ok=True)
    db_session.global_init(
            echo=False,
            conn_str='sqlite:///./db/v0_money.sqlite',
        )

    router.message.register(echo)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
