"""Release: balance command

Revision ID: 117f3fa4475d
Revises: 3ce9177f3a5d
Create Date: 2023-07-18 23:54:43.040388

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '117f3fa4475d'
down_revision = '3ce9177f3a5d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    message = (
            'Демо!'
            '\n\n'
            'Появилась команда /balance . Без аргументов она выводит твой текущий '
            'баланс. Так же поддерживается сокращенная форма - /b .'
            '\n\n'
            'Если написать с аргументом /balance NUMBER, то твой баланс изменится на '
            'NUMBER. Поддерживаются только числа'
            '\n\n'
            'Для отображения баланса группы используй /group_balance или /gb'
        )
    stmt = f"""
    insert into releases(id, message, is_broadcasted) values (3, "{message}", 0)
    """
    op.execute(stmt)


def downgrade() -> None:
    stmt = 'delete from releases where id = 3'
    op.execute(stmt)
