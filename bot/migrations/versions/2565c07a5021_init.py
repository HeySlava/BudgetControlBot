"""Init

Revision ID: 2565c07a5021
Revises:
Create Date: 2023-07-22 16:35:59.607613

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '2565c07a5021'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
            'releases',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('message', sa.String(), nullable=False),
            sa.Column('is_broadcasted', sa.Boolean(), nullable=False),
            sa.PrimaryKeyConstraint('id', name=op.f('pk_releases'))
        )

    op.create_table(
            'users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('first_name', sa.String(), nullable=False),
            sa.Column('last_name', sa.String(), nullable=True),
            sa.Column('username', sa.String(), nullable=True),
            sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
        )
    op.create_table(
            'items',
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(
                ['user_id'], ['users.id'], name=op.f('fk_items_user_id_users'),
            ),
            sa.PrimaryKeyConstraint('name', name=op.f('pk_items'))
        )

    op.create_table(
            'expenses',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('item_name', sa.String(), nullable=True),
            sa.Column('price', sa.Integer(), nullable=False),
            sa.Column('comment', sa.String(), nullable=True),
            sa.Column('cdate', sa.DateTime(), nullable=False),
            sa.Column('cdate_tz', sa.DateTime(), nullable=True),
            sa.Column('is_replenishment', sa.Boolean(), nullable=False),
            sa.ForeignKeyConstraint(
                ['item_name'], ['items.name'], name=op.f('fk_expenses_item_name_items'),
            ),
            sa.ForeignKeyConstraint(
                ['user_id'], ['users.id'], name=op.f('fk_expenses_user_id_users'),
            ),
            sa.PrimaryKeyConstraint('id', name=op.f('pk_expenses'))
        )


def downgrade() -> None:
    op.drop_table('expenses')
    op.drop_table('items')
    op.drop_table('users')
    op.drop_table('releases')
