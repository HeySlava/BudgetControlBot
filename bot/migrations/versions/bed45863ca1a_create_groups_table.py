"""Create groups table

Revision ID: bed45863ca1a
Revises: be53b2225cff
Create Date: 2023-07-10 19:46:05.727163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bed45863ca1a'
down_revision = 'be53b2225cff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
            'groups',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('cdate', sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint('id', name=op.f('pk_groups'))
        )
    with op.batch_alter_table('expenses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('group_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
                batch_op.f('fk_expenses_group_id_groups'),
                'groups',
                ['group_id'], ['id'],
            )

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('group_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
                batch_op.f('fk_users_group_id_groups'),
                'groups',
                ['group_id'], ['id'],
            )


def downgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(
                batch_op.f('fk_users_group_id_groups'), type_='foreignkey',
            )
        batch_op.drop_column('group_id')

    with op.batch_alter_table('expenses', schema=None) as batch_op:
        batch_op.drop_constraint(
                batch_op.f('fk_expenses_group_id_groups'), type_='foreignkey',
            )
        batch_op.drop_column('group_id')

    op.drop_table('groups')
