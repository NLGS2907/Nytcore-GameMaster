from logging import INFO
from typing import TYPE_CHECKING

from .loggers import (
    DISCORD_NAMESPACE,
    PEEWEE_MIGRATE_NAMESPACE,
    PEEWEE_NAMESPACE,
    config_logger,
    get_gamemaster_logger,
)

if TYPE_CHECKING:
    from logging import Logger


class LoggerManager:
    """Object for storing and managing the logs of the application."""

    def __init__(self,
                 *,
                 console_lvl: int=INFO,
                 only_bot_logger: bool=False):
        """Initializes the logger manager.
        
        Args:
            console_lvl: The preferred level to use for stream handlers.
            only_bot_logger: Wether to use the bot own logger and nothing else, or include the
                             other libraries in streams handlers.
        """

        self.gamemaster: "Logger" = get_gamemaster_logger(console_lvl)

        actual_lvl = (None if only_bot_logger else console_lvl)
        self.discord: "Logger" = config_logger(DISCORD_NAMESPACE, console_level=actual_lvl)
        self.db: "Logger" = config_logger(PEEWEE_NAMESPACE, console_level=actual_lvl)
        self.db_migrate: "Logger" = config_logger(PEEWEE_MIGRATE_NAMESPACE,
                                                  console_level=actual_lvl)
