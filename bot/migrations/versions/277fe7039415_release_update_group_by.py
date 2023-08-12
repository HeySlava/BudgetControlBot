"""release: update group by

Revision ID: 277fe7039415
Revises: 1dd516d556c2
Create Date: 2023-08-12 17:48:11.944061

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '277fe7039415'
down_revision = '1dd516d556c2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    msg = (
            'Обновление:'
            '\n\n'
            'Исправлена ошибка для репортов "Группировка по дню", "Группировка по кате'
            'гории". Теперь, если в один день были использованы разные валюты, это буд'
            'ет учтено'
        )
    stmt = f"insert into releases(id, message, is_broadcasted) values (6, '{msg}', 0)"
    op.execute(stmt)


def downgrade() -> None:
    stmt = 'delete from releases where id = 6'
    op.execute(stmt)
