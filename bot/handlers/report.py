from typing import List

import pytz
from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from sqlalchemy.orm import Session

from data import db_session
from data.models import User
from services import other


router = Router()

tz = pytz.timezone('Asia/Yerevan')


def _prepare_report(session: Session) -> List[str]:
    rows = other.get_report(session)
    chunk_size = 50
    report_lines = []
    for row in rows:
        to_yerevan_tz = (
                row.Expence.cdate
                .replace(tzinfo=pytz.UTC)
                .astimezone(tz)
                .strftime('%d.%m %H:%M')
            )
        txt = (
                f'{row.User.first_name}  {row.Expence.item_name}  '
                f'{row.Expence.price }  '
                f'{to_yerevan_tz}'
            )
        report_lines.append(txt.strip())

    chunks = [
            report_lines[i:i+chunk_size]
            for i in range(0, len(report_lines), chunk_size)
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
