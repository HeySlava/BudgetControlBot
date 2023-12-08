"""Report by month release

Revision ID: 09d3b6f33b87
Revises: 277fe7039415
Create Date: 2023-12-08 22:48:55.609781

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '09d3b6f33b87'
down_revision = '277fe7039415'
branch_labels = None
depends_on = None


def upgrade() -> None:
    msg = (
            'Обновление:'
            '\n\n'
            'Доступна группировка по месяцу для отчета'
        )
    stmt = f"insert into releases(id, message, is_broadcasted) values (7, '{msg}', 0)"
    op.execute(stmt)


def downgrade() -> None:
    stmt = 'delete from releases where id = 7'
    op.execute(stmt)
