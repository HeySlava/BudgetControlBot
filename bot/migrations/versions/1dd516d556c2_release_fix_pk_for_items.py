"""release: fix pk for items

Revision ID: 1dd516d556c2
Revises: da2917cd34a9
Create Date: 2023-07-26 01:49:23.494603

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '1dd516d556c2'
down_revision = 'da2917cd34a9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    msg = (
            'Обновление:'
            '\n\n'
            'Исправлена ошибка при добавлении новой категории'
        )
    stmt = f"insert into releases(id, message, is_broadcasted) values (5, '{msg}', 0)"
    op.execute(stmt)


def downgrade() -> None:
    stmt = 'delete from releases where id = 5'
    op.execute(stmt)
