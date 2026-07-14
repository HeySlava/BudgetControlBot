import asyncio
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

import pytest
from aiogram.types import CallbackQuery
from aiogram.types import Message
from handlers.report import cmd_report
from handlers.report import show_month_list

from testing.util import fill_in_db
from testing.util import get_random_user


class DummyObj:
    pass


@pytest.fixture
def mock_callback_query():
    cb = MagicMock(spec=CallbackQuery)
    cb.data = 'dummy_data'
    cb.answer = AsyncMock()
    cb.message = MagicMock()
    cb.message.chat = DummyObj()
    cb.message.edit_text = AsyncMock()
    cb.message.answer = AsyncMock()

    user = DummyObj()
    user.id = 1
    cb.from_user = user
    return cb


@pytest.fixture
def mock_message():
    message = MagicMock(spec=Message)
    message.chat = DummyObj()
    message.chat.id = 1
    message.answer = AsyncMock()
    return message


def test_cmd_report_renders_current_month(mock_message, db):
    fill_in_db(session=db, users_number=1, items_number=1, expenses_number=5)
    user = get_random_user(db)
    mock_message.chat.id = user.id

    asyncio.run(cmd_report(message=mock_message, session=db))

    mock_message.answer.assert_called_once()
    kwargs = mock_message.answer.call_args.kwargs
    assert 'Всего:' in kwargs['text']
    assert kwargs['reply_markup'] is not None


def test_show_month_list_renders_interactive_text(mock_callback_query, db):
    fill_in_db(session=db, users_number=1, items_number=1, expenses_number=5)
    user = get_random_user(db)
    mock_callback_query.from_user.id = user.id
    mock_callback_query.data = 'report:month:list:0'

    asyncio.run(show_month_list(cb=mock_callback_query, session=db))

    mock_callback_query.message.edit_text.assert_called_once()
    kwargs = mock_callback_query.message.edit_text.call_args.kwargs
    assert 'Выбери месяц' in kwargs['text']
    assert kwargs['reply_markup'] is not None
