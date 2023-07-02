"""Add comment column to expences

Revision ID: 045f5c05f2e1
Revises: b1fb2c7134e7
Create Date: 2023-07-02 17:37:07.419053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '045f5c05f2e1'
down_revision = 'b1fb2c7134e7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('expences', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comment', sa.String(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('expences', schema=None) as batch_op:
        batch_op.drop_column('comment')
