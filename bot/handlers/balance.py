import sqlalchemy as sa
from aiogram import Router
from aiogram.filters import CommandObject
from aiogram.filters.command import Command
from aiogram.types import Message
from sqlalchemy.orm import Session

from config import config
from data.models import Expense
from handlers._responses import RESPONSES
from services import expense_service
from services import user_service


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

            user = user_service.get_user_by_id(
                    user_id=message.chat.id,
                    session=session,
                )

            expense_service.add_expense(
                    user_id=message.chat.id,
                    is_replenishment=True,
                    item_name=config.replenishment_name,
                    price=value,
                    unit=user.currency,
                    session=session,
               )
            text = RESPONSES['new_replanishment'].format(
                    value=value,
                    currency=user.currency,
                )
            await message.answer(text)
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
        text = 'Изменить баланс - /balance ЧИСЛО\n\n'

        text += RESPONSES['current_balance'].format(
                balance=balance if balance else 0,
                currency=user.currency,
            )
        await message.answer(text)
