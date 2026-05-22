from typing import TYPE_CHECKING, Optional

from discord.ui import LayoutView

if TYPE_CHECKING:
    from ...gamemaster import GameMaster


class BaseGameView[GameType](LayoutView):
    """Base view for a game."""

    def __init__(self,
                 bot: "GameMaster",
                 game: GameType,
                 *,
                 timeout: Optional[float]=None):
        """Initializes the game view.
        
        Args:
            bot: A reference to the bot user.
            game: The game object.
        """

        super().__init__(timeout=timeout)

        self.bot: "GameMaster" = bot
        self.game: GameType = game
