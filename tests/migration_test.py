import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script
from alembic.script import ScriptDirectory

from conftest import base_dir


def get_revisions():

    revisions_dir = ScriptDirectory(f'{base_dir}/migrations')

    # Get & sort migrations, from first to last
    revisions = list(revisions_dir.walk_revisions('base', 'heads'))
    revisions.reverse()
    return revisions


def get_rev_ids(revision: Script) -> str:
    return revision.doc


@pytest.mark.parametrize('revision', get_revisions(), ids=get_rev_ids)
def test_migrations_stairway(alembic_config: Config, revision: Script):
    upgrade(alembic_config, revision.revision)
    downgrade(alembic_config, revision.down_revision or '-1')
    upgrade(alembic_config, revision.revision)
