"""Setup is_replaneshment column

Revision ID: 068ac5d35a1a
Revises: 7bd213a55a87
Create Date: 2023-07-15 23:01:12.281020

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '068ac5d35a1a'
down_revision = '7bd213a55a87'
branch_labels = None
depends_on = None


def upgrade() -> None:
    stmt = """
    UPDATE expenses
    set is_replenishment=subquery.is_replenishment
    from (
        select
             id
             , case
                when item_name = 'ОБМЕННИК' then 1
                else 0
            end is_replenishment
        from expenses
    ) subquery
    where expenses.id = subquery.id
    """
    op.execute(stmt)


def downgrade() -> None:
    stmt = 'UPDATE expenses set is_replenishment=0'
    op.execute(stmt)
