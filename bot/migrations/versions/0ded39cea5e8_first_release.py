"""First release

Revision ID: 0ded39cea5e8
Revises: ddfcd930779c
Create Date: 2023-07-10 23:07:27.397883

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from data.models import Release


# revision identifiers, used by Alembic.
revision = '0ded39cea5e8'
down_revision = 'ddfcd930779c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    session = Session(bind=op.get_bind())
    release = Release(
            id=1,
            message=(
                'Теперь новые информация об новых обновлениях будет приходить '
                'таким образом.\n\n'
                'Скоро появится баланс. Это поможет считать среднее, а так же остаток'
            )
        )
    session.add(release)
    session.commit()


def downgrade() -> None:
    session = Session(bind=op.get_bind())
    session.execute(sa.delete(Release).where(Release.id == 1))
