"""The module for holding the GameMaster."""

from os import getenv
from typing import TYPE_CHECKING, TypeAlias

from discord import Intents
from discord.ext.commands import Bot
from discord.utils import utcnow

if TYPE_CHECKING:
    from datetime import datetime

VersionTuple: TypeAlias = tuple[int, int, int]


class GameMaster(Bot):
    """The bot class for the GameMaster."""

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
