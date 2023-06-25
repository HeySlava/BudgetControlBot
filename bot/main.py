import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.types import Message
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
from services import category_service
from services import item_service


logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.token.get_secret_value())
dp = Dispatcher()


class newExpence(StatesGroup):
    choosing_category = State()
    choosing_item = State()
    writing_category = State()
    writing_item = State()


@dp.message(Command('start'))
async def cmd_start(message: Message):
    session = db_session.create_session()
    if message.from_user:
        user = user_service.register_user(
                id=message.from_user.id,
                first_name=message.from_user.first_name,
                session=session,
            )
        print(user)

    await message.answer('Hello!')


@dp.message(Command('new'))
async def new(message: Message):
    session = db_session.create_session()
    categories = category_service.get_list(session)
    kb = keyboards.get_category_kb(categories)
    await message.answer(
            text='Выбери категорию',
            reply_markup=kb,
        )


@dp.callback_query(Text('new_category'))
async def add_new_category(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Теперь напиши название новой категории')
    await callback.answer(
        show_alert=False,
    )
    await state.set_state(newExpence.writing_category)


@dp.callback_query(Text('new_item'))
async def add_new_item(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Теперь напиши название нового товара')
    await callback.answer(
        show_alert=False,
    )
    await state.set_state(newExpence.writing_item)


@dp.callback_query(Text(startswith='category'))
async def callbacks_num(cb: CallbackQuery, state: FSMContext):
    # TODO
    category_name = cb.data.split(':')[-1]
    await state.update_data(chosen_category=category_name)
    await state.set_state(newExpence.choosing_item)
    await cb.answer()

    session = db_session.create_session()
    items = item_service.get_list(session)
    kb = keyboards.get_items_kb(items)

    if cb.message:
        await cb.message.edit_text(text='Выбери товар')
        await cb.message.edit_reply_markup(reply_markup=kb)


@dp.message(newExpence.writing_item)
async def writing_new_item(m: Message, state: FSMContext):
    session = db_session.create_session()
    if m.text:
        item_service.add_item(
                item_name=m.text,
                session=session,
            )

        await m.answer(
                text=f'Добавлена новая позиция {m.text!r}\n\n/new',
        )
    await state.clear()


@dp.message(newExpence.writing_category)
async def writing_new_category(m: Message, state: FSMContext):
    session = db_session.create_session()
    if m.text:
        category_service.add_category(
                category_name=m.text,
                session=session,
            )

        categories = category_service.get_list(session)
        kb = keyboards.get_category_kb(categories)
        await m.answer(
                text=f'Добавлена категорию {m.text!r}',
                reply_markup=kb,
        )
    await state.clear()


@dp.callback_query()
async def echo_callback(callback: CallbackQuery):
    await callback.message.answer(f'Ответ на каллбек {callback.data}')
    await callback.answer(
        text='Спасибо, что воспользовались ботом!',
        show_alert=False,
    )


async def echo(message: Message):
    if message.text:
        await message.answer(message.text)


async def main():
    db_session.global_init(
            echo=True,
            conn_str='sqlite://',
        )
    dp.message.register(echo)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
