from typing import List

import pytz
from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from sqlalchemy.orm import Session

from data import db_session
from data.models import User
from services import expence_service
from services import other


router = Router()

tz = pytz.timezone('Asia/Yerevan')


def _prepare_report(session: Session) -> List[str]:
    expences = expence_service.get_expences(session)
    report_lines = []
    for expence in expences:
        to_yerevan_tz = (
                expence.cdate
                .replace(tzinfo=pytz.UTC)
                .astimezone(tz)
                .strftime('%d.%m %H:%M')
            )
        txt = (
                f'{expence.user.first_name}  {expence.item_name}  '
                f'{expence.price }  {to_yerevan_tz}'
            )
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
    session = db_session.create_session()
    for msg in _prepare_report(session):
        await message.answer(msg)


@router.message(Command('test'))
async def cmd_test(message: Message):
    session = db_session.create_session()
    rows = other.get_report_by(
            session,
            # group_by=func.date(Expence.cdate),
            group_by=User.first_name,
        )
    for row in rows:
        await message.answer(row)
