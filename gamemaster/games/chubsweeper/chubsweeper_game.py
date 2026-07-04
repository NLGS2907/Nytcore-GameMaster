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
        self._dealer, self._miners = self._distinguish_players()


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


    def _distinguish_players(self) -> tuple["Player", list["Player"]]:
        """Tries to separate the host player from the rest.
        
        Raises:
            ValueError: If, somehow, the host user isn't in the player's list.

        Returns:
            A tuple where the first element is the host user (a.k.a. the \"Dealer\"), and the
            second element is a list of the rest of the players (i.e. the \"Miners\").
        """

        dealer = None
        miners = []
        for player in self.players:
            if player.discord_user_id == self.host_user.id:
                dealer = player
            else:
                miners.append(player)

        if dealer is None:
            raise ValueError("No dealer detected in this game. "
                             f"It should be the user with id {self.host_user.id!r}")

        return dealer, miners


    @property
    def dealer(self) -> "Player":
        """Fetches the host user of this game."""

        return self._dealer


    @property
    def miners(self) -> list["Player"]:
        """Fetches the players of this game, other than the host."""

        return self._miners
