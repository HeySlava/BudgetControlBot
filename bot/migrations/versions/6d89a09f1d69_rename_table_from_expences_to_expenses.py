"""Rename table from expences to expenses

Revision ID: 6d89a09f1d69
Revises: 045f5c05f2e1
Create Date: 2023-07-02 18:22:19.123146

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '6d89a09f1d69'
down_revision = '045f5c05f2e1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table('expences', 'expenses')


def downgrade() -> None:
    op.rename_table('expenses', 'expences')
