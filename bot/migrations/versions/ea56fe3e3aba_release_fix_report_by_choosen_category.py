"""release: fix report by choosen category

Revision ID: ea56fe3e3aba
Revises: 8fd8e46090ac
Create Date: 2023-07-23 23:03:23.912832

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'ea56fe3e3aba'
down_revision = '8fd8e46090ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    msg = (
            'Исравление:'
            '\n\n'
            'Востановлена функциональность отображения '
            'расходов по выборанной категории.'
        )
    stmt = f"insert into releases(id, message, is_broadcasted) values (3, '{msg}', 0)"
    op.execute(stmt)


def downgrade() -> None:
    stmt = 'delete from releases where id = 3'
    op.execute(stmt)
