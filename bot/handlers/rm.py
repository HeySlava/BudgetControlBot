from typing import Tuple

from aiogram import Router
from aiogram.filters import CommandObject
from aiogram.filters.command import Command
from aiogram.types import Message
from services import rm_service
from sqlalchemy.orm import Session


router = Router()


class WrongRmCommand(ValueError):
    pass


def _parse_rm_command(args: str | None) -> Tuple[str, str]:
    if not args:
        raise WrongRmCommand
    command_type, _, category = args.partition(' ')
    category = category.strip("'").strip('"')
    if command_type != 'category':
        raise WrongRmCommand
    return command_type, category


async def _delete_category(message: Message, session: Session, command: CommandObject):
    try:
        _, category = _parse_rm_command(command.args)
    except WrongRmCommand:
        return await message.answer(f'Неверная команда {command.args!r}')

    try:
        rm_service.rm_empty_category(
                user_id=message.chat.id,
                item_name=category.upper(),
                session=session,
            )
    except rm_service.WrongCategoryError:
        msg = f'Категории {category!r} не найдено'
    except rm_service.NotEmptyCategoryError:
        msg = 'Временно нельзя удалить категорию, для которой есть записи'
    else:
        msg = f'Категория {category!r} удалена'
    return await message.answer(msg)


@router.message(Command('rm'))
async def rm_category(message: Message, session: Session, command: CommandObject):
    if not command.args:
        return await message.answer('Укажи категорию')

    return await _delete_category(message=message, session=session, command=command)
