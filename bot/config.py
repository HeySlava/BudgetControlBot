import pytz
import configparser

from pathlib import Path
from dataclasses import dataclass

_CONFIG_INI_PATH = Path(__file__).absolute().parent.parent / 'config.ini'
_default_token = '22:aa-F-6eNoKY65R-omFA'
_admin_id = 123

configreader = configparser.ConfigParser()
if not _CONFIG_INI_PATH.exists():
    token = _default_token
    admin = _admin_id
else:
    configreader.read(_CONFIG_INI_PATH)
    try:
        admin = int(configreader['config']['admin'])
        token = configreader['config']['token']
    except (KeyError, ValueError):
        print(f"You didn't setup your {_CONFIG_INI_PATH}. See example.config.ini")
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
