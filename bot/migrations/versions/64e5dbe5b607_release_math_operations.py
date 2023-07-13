"""release: math operations

Revision ID: 64e5dbe5b607
Revises: 0ded39cea5e8
Create Date: 2023-07-14 02:01:30.052661

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

from data.models import Release


# revision identifiers, used by Alembic.
revision = '64e5dbe5b607'
down_revision = '0ded39cea5e8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    session = Session(bind=op.get_bind())
    release = Release(
            id=2,
            message=(
                'ОБНОВЛЕНИЕ!'
                '\n\n'
                'При добавление новой записи теперь возможно записывать математические'
                " выражения. Поддерживаются только целые числа и знаки '-', '+'."
                '\n\n'
                'Примеры:'
                '\n'
                '100 + 200'
                '\n'
                '100 +200'
                '\n'
                '100 + 200 + 300 + 500'
                '\n'
                '100 - 200'
            )
        )
    session.add(release)
    session.commit()


def downgrade() -> None:
    session = Session(bind=op.get_bind())
    session.execute(sa.delete(Release).where(Release.id == 2))
