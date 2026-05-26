from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING

from .date_fmt import _DEFAULT_DATE_FMT, _DateFormatter


class StreamFormatter(_DateFormatter):
    # ANSI codes are a bit weird to decipher if you're unfamiliar with them, so here's a refresher
    # It starts off with a format like \x1b[XXXm where XXX is a semicolon separated list of commands
    # The important ones here relate to colour.
    # 30-37 are black, red, green, yellow, blue, magenta, cyan and white in that order
    # 40-47 are the same except for the background
    # 90-97 are the same but "bright" foreground
    # 100-107 are the same as the bright ones but for the background.
    # 1 means bold, 2 means dim, 0 means reset, and 4 means underline.
    LEVEL_COLOURS = [
        (DEBUG, '\x1b[40;1m'),
        (INFO, '\x1b[34;1m'),
        (WARNING, '\x1b[33;1m'),
        (ERROR, '\x1b[31m'),
        (CRITICAL, '\x1b[41m'),
    ]

    FORMATS = {
        level: _DateFormatter(
            f"\x1b[30;1m%(asctime)-26s\x1b[0m - {colour}%(levelname)-8s\x1b[0m - [ \x1b[35m%(name)s\x1b[0m ] %(message)s",
            _DEFAULT_DATE_FMT,
        )
        for level, colour in LEVEL_COLOURS
    }


    def format(self, record):
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[DEBUG]

        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f'\x1b[31m{text}\x1b[0m'

        output = formatter.format(record)

        record.exc_text = None
        return output
