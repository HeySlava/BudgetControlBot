import configparser
from dataclasses import dataclass
from pathlib import Path

import pytz

_CONFIG_INI_PATH = Path(__file__).absolute().parent.parent / 'config.ini'

configreader = configparser.ConfigParser()
_error_msg = f'Setup {_CONFIG_INI_PATH} for work. See example.config.ini'
if not _CONFIG_INI_PATH.exists():
    print(_error_msg)
    raise SystemExit(1)

configreader.read(_CONFIG_INI_PATH)
try:
    admin = int(configreader['config']['admin'])
    token = configreader['config']['token']
except (KeyError, ValueError):
    print(_error_msg)
    raise SystemExit(1)


@dataclass
class Config:
    token: str = token
    admin: int = admin
    conn_str: str = 'sqlite:///./db/budget.sqlite'
    migration_script_location: Path = Path(__file__).parent / 'migrations'
    alembic_config_path: Path = Path(__file__).parent / 'alembic.ini'
    tz = pytz.timezone('Asia/Yerevan')
    last: int = 10
    replenishment_name: str = '_replenishemnt'


config = Config()
