from typing import List
from typing import Sequence

from aiogram import Router
from aiogram.filters import CommandObject
from aiogram.filters.command import Command
from aiogram.types import Message
from config import config
from data.models import Expense
from handlers._responses import RESPONSES
from services import balance_service
from services import expense_service
from services import user_service
from sqlalchemy.orm import Session
from utils import chunkineze


router = Router()


def _prepare_balance_history(replenishments: Sequence[Expense]) -> List[str]:
    report_lines = []
    if not replenishments:
        report_lines.append('Здесь пока пусто')

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


async def _just_balance(
        message: Message,
        session: Session,
) -> None:
    user = user_service.get_user_by_id(message.chat.id, session)
    balance = balance_service.get_balance(user.id, session)
    text = 'Изменить баланс на ЧИСЛО - /balance ЧИСЛО\n\n'

    text += RESPONSES['current_balance'].format(
            balance=balance,
            currency=user.currency,
        )
    return await message.answer(text)


async def _balance_history(
        message: Message,
        session: Session,
) -> None:

    replenishments = balance_service.get_balance_history(
            user_id=message.chat.id,
            session=session,
        )
    for chunk in _prepare_balance_history(replenishments):
        await message.answer(chunk)


def _replanishment_msg(
        value: int,
        currency: str,
) -> str:
    if value >= 0:
        text = RESPONSES['new_replanishment'].format(
                value=value,
                currency=currency,
            )
    else:
        text = RESPONSES['new_expence'].format(
                value=value,
                currency=currency,
            )
    return text


@router.message(Command('b'))
@router.message(Command('balance'))
async def balance(message: Message, session: Session, command: CommandObject):
    if not command.args:
        await _just_balance(message=message, session=session)

    if command.args.strip() == 'history':
        return await _balance_history(message=message, session=session)

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
        text = _replanishment_msg(
                value=value,
                currency=user.currency,
            )
        await message.answer(text)
