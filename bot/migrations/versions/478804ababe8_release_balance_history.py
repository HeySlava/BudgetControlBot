"""release: balance history

Revision ID: 478804ababe8
Revises: ea56fe3e3aba
Create Date: 2023-07-24 21:53:28.212514

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '478804ababe8'
down_revision = 'ea56fe3e3aba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    msg = (
            'Обновление:'
            '\n\n'
            'Теперь для команды /balance ЧИСЛО можно добавить комментарий. '
            'Все что будет с новой строки, будет расцениваться как комментарий'
            '\n\n'
            'Пример:'
            '\n'
            '/balance 100'
            '\n'
            'Демонстрационный комментарий'
            '\n\n'
            'Для команды /balance появилась опция history для отображения истории '
            'пополнений'
            '\n\n'
            'Пример: /balance history'
        )
    stmt = f"insert into releases(id, message, is_broadcasted) values (4, '{msg}', 0)"
    op.execute(stmt)


def downgrade() -> None:
    stmt = 'delete from releases where id = 4'
    op.execute(stmt)
