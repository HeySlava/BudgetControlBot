import asyncio
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

import pytest
from aiogram.types import CallbackQuery
from handlers.report import cb_reports_menu
from handlers.report import group_by_category
from handlers.report import group_by_month
from handlers.report import report_last

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


def test_reports_menu_renders_correctly(mock_callback_query):
    # Test that the reports menu handler uses edit_text
    asyncio.run(cb_reports_menu(mock_callback_query))

    mock_callback_query.message.edit_text.assert_called_once()
    kwargs = mock_callback_query.message.edit_text.call_args.kwargs
    assert kwargs['text'] == 'Выбери тип отчета'
    assert kwargs['reply_markup'] is not None


def test_last_n_renders_interactive_text(mock_callback_query, db):
    fill_in_db(session=db, users_number=1, items_number=1, expenses_number=5)
    user = get_random_user(db)
    mock_callback_query.from_user.id = user.id
    mock_callback_query.message.chat.id = user.id

    asyncio.run(report_last(update=mock_callback_query, session=db))

    mock_callback_query.message.edit_text.assert_called_once()
    kwargs = mock_callback_query.message.edit_text.call_args.kwargs
    assert 'Последние' in kwargs['text']
    assert 'записей:' in kwargs['text']
    assert kwargs['reply_markup'] is not None  # Should have the back button


def test_group_by_category_renders_interactive_text(mock_callback_query, db):
    fill_in_db(session=db, users_number=1, items_number=2, expenses_number=5)
    user = get_random_user(db)
    mock_callback_query.from_user.id = user.id

    asyncio.run(group_by_category(cb=mock_callback_query, session=db))

    mock_callback_query.message.edit_text.assert_called_once()
    kwargs = mock_callback_query.message.edit_text.call_args.kwargs
    assert 'Расходы по категориям' in kwargs['text']
    assert kwargs['reply_markup'] is not None


def test_group_by_month_renders_interactive_text(mock_callback_query, db):
    fill_in_db(session=db, users_number=1, items_number=1, expenses_number=5)
    user = get_random_user(db)
    mock_callback_query.from_user.id = user.id

    asyncio.run(group_by_month(cb=mock_callback_query, session=db))

    mock_callback_query.message.edit_text.assert_called_once()
    kwargs = mock_callback_query.message.edit_text.call_args.kwargs
    assert 'Всего:' in kwargs['text']
    assert kwargs['reply_markup'] is not None
