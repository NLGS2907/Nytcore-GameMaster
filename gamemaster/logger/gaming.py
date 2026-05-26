"""Configurations for custom gaming logger.

Attributes:
    GAMEMASTER_NAMESPACE: The default namespace for the custom logger.
    LOG_PATH: The default path for the custom logger.
"""

from logging import DEBUG, INFO, FileHandler, StreamHandler, getLogger
from logging import root as root_logger
from typing import TYPE_CHECKING

from .custom import FileFormatter, StreamFormatter

if TYPE_CHECKING:
    from logging import Logger

GAMEMASTER_NAMESPACE: str = "gamemaster"


def log_lvl(verbose: bool) -> int:
    """Returns the log level preferred, depending if we are in verbose mode or not."""

    return (DEBUG if verbose else INFO)


def get_log_path(namespace: str) -> str:
    """Gets the log filepath from the inteded namespace."""

    return f"./logs/{namespace}.log"


def _namespace_exists(name: str) -> bool:
    """Checks if a given namespace exists in the root logger registry.
    
    Args:
        name: The namespace to check.

    Returns:
        A boolean indicating if the namespace is present or not.
    """

    return name in root_logger.manager.loggerDict


def add_terminal_handler(logger: "Logger", *, console_level: int=INFO):
    """Adds a terminal handler to a given logger and sets its formatters.
    
    Args:
        logger: The logger to modify.
        console_level: The log level for the file handler.
    """

    terminal_handler = StreamHandler()
    terminal_handler.setLevel(console_level)
    terminal_handler.setFormatter(StreamFormatter.FORMATS[console_level])

    logger.addHandler(terminal_handler)


def get_gamemaster_logger(log_level: int=INFO) -> "Logger":
    """Gets the specific logger of the bot's namespace."""

    if _namespace_exists(GAMEMASTER_NAMESPACE):
        return getLogger(GAMEMASTER_NAMESPACE)

    return config_logger(console_level=log_level)


def add_file_handler(logger: "Logger", *, file_level: int=DEBUG):
    """Adds a file handler to a given logger and sets its formatters.
    
    Args:
        logger: The logger to modify.
        file_level: The log level for the file handler.
    """

    file_handler = FileHandler(filename=get_log_path(GAMEMASTER_NAMESPACE), encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(FileFormatter())

    logger.addHandler(file_handler)


def config_logger(*, file_level: int=DEBUG, console_level: int=INFO) -> "Logger":
    """Configures the default logger for the bot.

    Ideally, this should be called at least once, at the start of the bot's lifetime.
    
    Args:
        file_level: The log level for the file handler.
        console_level: The log level for the terminal handler.

    Returns:
        The logger that was generated. Alternatively, it can still be located with the same
        namespace in `getLogger()`.
    """

    logger = getLogger(GAMEMASTER_NAMESPACE)
    logger.setLevel(DEBUG)
    add_file_handler(logger, file_level=file_level)
    add_terminal_handler(logger, console_level=console_level)

    return logger
