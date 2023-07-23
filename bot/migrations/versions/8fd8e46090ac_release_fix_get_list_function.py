"""release: fix get_list function

Revision ID: 8fd8e46090ac
Revises: fc2b890a75ce
Create Date: 2023-07-23 12:10:56.086668

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '8fd8e46090ac'
down_revision = 'fc2b890a75ce'
branch_labels = None
depends_on = None


def upgrade() -> None:
    msg = (
            'Обновление:'
            '\n\n'
            'Корректное отображение категорий при команде /new. '
            'Ранее была утечка и отображались все категории все пользователей'
        )
    stmt = f"insert into releases(id, message, is_broadcasted) values (2, '{msg}', 0)"
    op.execute(stmt)


def downgrade() -> None:
    stmt = 'delete from releases where id = 2'
    op.execute(stmt)
