import datetime as dt
from typing import Optional


def try_datetime(string_dt: str) -> Optional[dt.date]:
    try:
        return dt.datetime.strptime(string_dt, '%Y-%m-%d').date()
    except ValueError:
        return None
