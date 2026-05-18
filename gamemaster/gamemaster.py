"""The module for holding the GameMaster."""

from logging import getLogger
from os import getenv
from typing import TYPE_CHECKING, TypeAlias

from discord import Intents
from discord.ext.commands import Bot
from discord.utils import utcnow

from .logger import add_file_handler, get_gamemaster_logger

if TYPE_CHECKING:
    from datetime import datetime
    from logging import Logger

VersionTuple: TypeAlias = tuple[int, int, int]


class GameMaster(Bot):
    """The bot class for the GameMaster.
    
    Attributes:
        booted_at: A timestamp to know when was the bot booted up.
        log: A comfortable reference to the custom logger. Besides this one, one can always
             retrieve it using `getLogger()` with the bot namespace.
        ds_log: A reference to a secondary, special logger used by the discord.py library itself. 
    """

    @staticmethod
    def version() -> VersionTuple:
        """Returns the version information as a tuple.
        
        The format is (X, Y, Z) where:
        * X is the major patch
        * Y is a minor patch
        * Z is a small fix
        """

        return (0, 0, 1)

    @staticmethod
    def preferred_intents() -> Intents:
        """Reports the event buses that the gamemaster intends to subscribe to."""

        return Intents.all()


    def __init__(self, verbose: bool=True, **options):
        """Initializes the GameMaster.
        
        Args:
            verbose: Elevates the log level to show everything.
            **options: Extra options to pass on to the parent initializer.
        """

        super().__init__("!", # Deprecated, but legacy syntax requires it
                         intents=GameMaster.preferred_intents(),
                         application_id=getenv("BOT_ID"),
                         options=options)

        self.booted_at: "datetime" = utcnow()
        self.log: "Logger" = get_gamemaster_logger()
        self.ds_log: "Logger" = getLogger("discord")

        add_file_handler(self.ds_log)
