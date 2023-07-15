"""Fill in balance

Revision ID: 74260b1ce7a1
Revises: 25b6523cb85d
Create Date: 2023-07-15 15:44:52.608824

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '74260b1ce7a1'
down_revision = '25b6523cb85d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    stmt = """
    UPDATE users
    SET balance=(-subquery.total)
    FROM (
        SELECT expenses.user_id AS user_id, sum(expenses.price) AS total
        FROM expenses GROUP BY expenses.user_id
    ) AS subquery
    WHERE users.id = subquery.user_id
    """
    op.execute(stmt)


def downgrade() -> None:
    stmt = 'UPDATE users SET balance=0'
    op.execute(stmt)
