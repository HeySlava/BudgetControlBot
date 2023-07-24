from typing import List
from typing import Sequence

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
from services import balance_service
from utils import chunkineze


router = Router()


def _prepare_balance_history(replenishments: Sequence[Expense]) -> List[str]:
    report_lines = []
    for replenishment in replenishments:
        cdate_tz_formatted = replenishment.cdate_tz.strftime('%d.%m %H:%M')
        txt = (
                f'{replenishment.user.first_name}  '
                f'{replenishment.price} {replenishment.unit}  {cdate_tz_formatted}'
            )
        if replenishment.comment:
            txt += f'  {replenishment.comment}'
        report_lines.append(txt.strip())

    return chunkineze(report_lines, chunk_size=50)


@router.message(Command('b'))
@router.message(Command('balance'))
async def balance(message: Message, session: Session, command: CommandObject):
    if not command.args:
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
        text = 'Изменить баланс на ЧИСЛО - /balance ЧИСЛО\n\n'

        text += RESPONSES['current_balance'].format(
                balance=balance if balance else 0,
                currency=user.currency,
            )
        return await message.answer(text)

    if command.args.strip() == 'history':
        replenishments = balance_service.get_balance_history(
                user_id=message.chat.id,
                session=session,
            )
        for chunk in _prepare_balance_history(replenishments):
            await message.answer(chunk)
            return

    value, _, comment = command.args.partition('\n')
    try:
        value = int(value)
    except ValueError:
        await message.answer(f'Неправильный аргумент: {value!r}')
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
                comment=comment.strip(),
                unit=user.currency,
                session=session,
           )
        text = RESPONSES['new_replanishment'].format(
                value=value,
                currency=user.currency,
            )
        await message.answer(text)
