from datetime import datetime
from logging import Formatter

_DEFAULT_DATE_FMT: str = "%Y-%m-%d %H:%M:%S.%f"


class _DateFormatter(Formatter):
    """Custom date formatter, for showing microseconds."""

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created)
        if datefmt:
            return dt.strftime(datefmt)

        return dt.strftime(_DEFAULT_DATE_FMT)