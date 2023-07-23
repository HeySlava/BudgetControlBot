"""release: fix currency

Revision ID: fc2b890a75ce
Revises: eae5697ecefa
Create Date: 2023-07-23 11:11:54.778593

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'fc2b890a75ce'
down_revision = 'eae5697ecefa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    msg = (
            'Обновление:'
            '\n\n'
            'Исправление ошибка отображения валюты при отчете и добавлении новой '
            'записи.'
            '\n\n'
            'При отчете с группировкой, где использовались разные валюты в течение '
            'выбранного периода - сохраняется.'
        )
    stmt = f"insert into releases(id, message, is_broadcasted) values (1, '{msg}', 0)"
    op.execute(stmt)


def downgrade() -> None:
    stmt = 'delete from releases where id = 1'
    op.execute(stmt)
