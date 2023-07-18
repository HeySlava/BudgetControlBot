import sqlalchemy as sa
from aiogram import Router
from aiogram.filters import CommandObject
from aiogram.filters.command import Command
from aiogram.types import Message
from sqlalchemy.orm import Session

import utils
from data.models import Expense
from services import user_service
from services import expense_service


router = Router()


@router.message(Command('b'))
@router.message(Command('balance'))
async def balance(message: Message, session: Session, command: CommandObject):
    if command.args:
        try:
            value = int(command.args)
        except ValueError:
            await message.answer('Неправильный аргумент')
        else:
            expense_service.add_expense(
                    user_id=message.chat.id,
                    is_replenishment=True,
                    price=value,
                    session=session,
               )
            await message.answer(f'Новое пополнение на {value!r}')
    else:
        user = user_service.get_user_by_id(message.chat.id, session)
        stmt = sa.select(
                sa.func.sum(
                    sa.case(
                        (
                            Expense.is_replenishment,
                            Expense.price,
                        ),
                        (
                            ~Expense.is_replenishment,
                            -Expense.price,
                        )
                    )
                )
            ).where(Expense.user_id == user.id)

        balance = session.execute(stmt).scalar()
        await message.answer(f'Your balance is {balance}')


@router.message(Command('gb'))
@router.message(Command('group_balance'))
async def group_balance(message: Message, session: Session):
    user = user_service.get_user_by_id(message.chat.id, session)

    user_ids = utils.get_ids_by_user(user)
    stmt = sa.select(
            sa.func.sum(
                sa.case(
                    (
                        Expense.is_replenishment,
                        Expense.price,
                    ),
                    (
                        ~Expense.is_replenishment,
                        -Expense.price,
                    )
                )
            )
        ).where(Expense.user_id.in_(user_ids))

    balance = session.execute(stmt).scalar()
    await message.answer(f'Your group balance is {balance}')
