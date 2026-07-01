from typing import TYPE_CHECKING, Optional

from ..game_base import BaseGame
from .chubsweeper_options import ChubSweeperOptions

if TYPE_CHECKING:
    from discord.abc import User

    from ...gamemaster import GameMaster
    from ...models import Player
    from ..game_base import EmojisCollection


class ChubSweeperGame(BaseGame[ChubSweeperOptions]):
    """Game class for a game of ChubSweeper.

    Attributes:
        bot: A reference to the bot user.
        host_user: The original user that started the game.
        players: A list of all the players involved in the game.
        options: The options object of this game, if available.
    """

    def __init__(self,
                 bot: "GameMaster",
                 host_user: "User",
                 players: list["Player"],
                 *,
                 options: ChubSweeperOptions):
        super().__init__(bot, host_user, players, options=options)


    @staticmethod
    def title_name() -> str:
        return "ChubSweeper"


    @staticmethod
    def description() -> Optional[str]:
        return "Try to avoid landing on the ChubMines™, while appreciating the \"safes\"."


    @staticmethod
    def emojis_collection() -> "EmojisCollection":
        return ["🤰🏻", "🫃🏻", "🫄🏻"]


    @staticmethod
    def minimum_players() -> int:
        return 2


    @staticmethod
    def maximum_players() -> int:
        return 9
