from typing import TYPE_CHECKING, Optional

from ..game_base import BaseGame
from .element_rps_options import ElementRPSOptions

if TYPE_CHECKING:
    from ..game_base import EmojisCollection


class ElementRPSGame(BaseGame[ElementRPSOptions]):
    """Game class for a game of Element Rock-Paper-Scissors.

    Attributes:
        bot: A reference to the bot user.
        host_user: The original user that started the game.
        players: A list of all the players involved in the game.
        options: The options object of this game, if available.
    """


    @staticmethod
    def title_name() -> str:
        return "Element Rock-Paper-Scissors"


    @staticmethod
    def description() -> Optional[str]:
        return "Classic game of Rock-Paper-Scissors, but with NIKKE's element codes!"


    @staticmethod
    def emojis_collection() -> "EmojisCollection":
        return [__class__.wind_emoji(),
                __class__.water_emoji(),
                __class__.iron_emoji(),
                __class__.fire_emoji(),
                __class__.electric_emoji()]


    @staticmethod
    def minimum_players() -> int:
        return 2


    @staticmethod
    def maximum_players() -> int:
        return 2


    @staticmethod
    def wind_emoji():
        """Returns the game's fallback emoji for the wind element."""

        return "💨"

    @staticmethod
    def water_emoji():
        """Returns the game's fallback emoji for the water element."""

        return "💦"

    @staticmethod
    def iron_emoji():
        """Returns the game's fallback emoji for the iron element."""

        return "🔩" # close enough

    @staticmethod
    def fire_emoji():
        """Returns the game's fallback emoji for the fire element."""

        return "🔥"

    @staticmethod
    def electric_emoji():
        """Returns the game's fallback emoji for the electric element."""

        return "⚡"
