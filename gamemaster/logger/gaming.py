"""Configurations for custom gaming logger.

Attributes:
    GAMEMASTER_NAMESPACE: The default namespace for the custom logger.
    LOG_PATH: The default path for the custom logger.
"""

from logging import DEBUG, INFO, FileHandler, Formatter, StreamHandler, getLogger
from typing import TYPE_CHECKING
from logging import root as root_logger

if TYPE_CHECKING:
    from logging import Logger

GAMEMASTER_NAMESPACE: str = "gamemaster"
LOG_PATH: str = f"./{GAMEMASTER_NAMESPACE}.log"
DEFAULT_FMT: str = "%(asctime)s - %(levelname)s - %(message)s"
DEFAULT_DATE_FMT: str = "%d-%m-%Y %I:%M:%S %p"


def _namespace_exists(name: str) -> bool:
    """Checks if a given namespace exists in the root logger registry.
    
    Args:
        name: The namespace to check.

    Returns:
        A boolean indicating if the namespace is present or not.
    """

    return name in root_logger.manager.loggerDict


def get_gamemaster_logger() -> "Logger":
    """Gets the specific logger of the bot's namespace."""

    if _namespace_exists(GAMEMASTER_NAMESPACE):
        return getLogger(GAMEMASTER_NAMESPACE)

    return config_logger()


def add_file_handler(logger: "Logger",
                     *,
                     file_level: int=DEBUG,
                     fmt: str=DEFAULT_FMT,
                     date_fmt: str=DEFAULT_DATE_FMT):
    """Adds a file handler to a given logger and sets its formatters.
    
    Args:
        logger: The logger to modify.
        file_level: The log level for the file handler.
        fmt: The general format for the log messages to have.
        date_fmt: How to further format the timestamp in the messages.
    """

    file_handler = FileHandler(filename=LOG_PATH, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(Formatter(fmt=fmt, datefmt=date_fmt))

    logger.addHandler(file_handler)


def add_terminal_handler(logger: "Logger",
                         *,
                         console_level: int=INFO,
                         fmt: str=DEFAULT_FMT,
                         date_fmt: str=DEFAULT_DATE_FMT):
    """Adds a terminal handler to a given logger and sets its formatters.
    
    Args:
        logger: The logger to modify.
        console_level: The log level for the file handler.
        fmt: The general format for the log messages to have.
        date_fmt: How to further format the timestamp in the messages.
    """

    terminal_handler = StreamHandler()
    terminal_handler.setLevel(console_level)
    terminal_handler.setFormatter(Formatter(fmt=fmt, datefmt=date_fmt))

    logger.addHandler(terminal_handler)


def config_logger(*,
                  file_level: int=DEBUG,
                  console_level: int=INFO,
                  fmt: str=DEFAULT_FMT,
                  date_fmt: str=DEFAULT_DATE_FMT) -> "Logger":
    """Configures the default logger for the bot.

    Ideally, this should be called at least once, at the start of the bot's lifetime.
    
    Args:
        file_level: The log level for the file handler.
        console_level: The log level for the terminal handler.
        fmt: The general format for the log messages to have.
        date_fmt: How to further format the timestamp in the messages.

    Returns:
        The logger that was generated. Alternatively, it can still be located with the same
        namespace in `getLogger()`.
    """

    logger = getLogger(GAMEMASTER_NAMESPACE)
    logger.setLevel(DEBUG)
    add_file_handler(logger, file_level=file_level, fmt=fmt, date_fmt=date_fmt)
    add_terminal_handler(logger, console_level=console_level, fmt=fmt, date_fmt=date_fmt)

    return logger
