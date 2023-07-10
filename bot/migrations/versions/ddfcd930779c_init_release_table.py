"""Init release table

Revision ID: ddfcd930779c
Revises: bed45863ca1a
Create Date: 2023-07-10 22:47:05.661443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddfcd930779c'
down_revision = 'bed45863ca1a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
            'releases',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('message', sa.String(), nullable=False),
            sa.Column('is_broadcasted', sa.Boolean(), nullable=False),
            sa.PrimaryKeyConstraint('id', name=op.f('pk_releases')),
        )


def downgrade() -> None:
    op.drop_table('releases')
