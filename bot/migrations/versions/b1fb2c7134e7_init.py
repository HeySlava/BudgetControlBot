"""Init

Revision ID: b1fb2c7134e7
Revises:
Create Date: 2023-07-01 09:42:45.539453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1fb2c7134e7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
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
                ['user_id'], ['users.id'],
                name=op.f('fk_items_user_id_users')),
            sa.PrimaryKeyConstraint('name', name=op.f('pk_items'))
        )
    op.create_table(
            'expences',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('item_name', sa.String(), nullable=False),
            sa.Column('price', sa.Integer(), nullable=False),
            sa.Column('cdate', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(
                ['item_name'], ['items.name'],
                name=op.f('fk_expences_item_name_items')),
            sa.ForeignKeyConstraint(
                ['user_id'], ['users.id'],
                name=op.f('fk_expences_user_id_users')),
            sa.PrimaryKeyConstraint('id', name=op.f('pk_expences'))
        )


def downgrade() -> None:
    op.drop_table('expences')
    op.drop_table('items')
    op.drop_table('users')