from pathlib import Path

from data.models import Expense
from data.models import Item
from data.models import User
from sqlalchemy import orm


base_dir = Path(__file__).parent.parent / 'bot'


def fill_in_db(
        session: orm.Session,
        users_number: int = 1,
        expenses_number: int = 1,
        items_number: int = 1,
        currencies: list = ['unit1'],
        commit: bool = True,
):
    for u in range(users_number):
        user = User(id=u, first_name=f'user-{u}')
        for i_num in range(items_number):
            item_name = str(i_num)
            item = Item(name=item_name)
            user.items.append(item)
            for unit in currencies:
                for e_num in range(expenses_number):
                    expense = Expense(item_name=item_name, price=100, unit=unit)
                    user.expenses.append(expense)
        session.add(user)
    if commit:
        session.commit()
    return session
