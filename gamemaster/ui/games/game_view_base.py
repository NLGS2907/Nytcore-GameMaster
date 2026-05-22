from typing import TYPE_CHECKING, Optional

from ..base_view import BaseView

if TYPE_CHECKING:
    from discord import InteractionMessage

    from ...gamemaster import GameMaster
    from ..base_view import PossibleUser


class BaseGameView[GameType](BaseView):
    """Base view for a game."""

    def __init__(self,
                 bot: "GameMaster",
                 parent_msg: "InteractionMessage",
                 origin_user: PossibleUser,
                 game: GameType,
                 *,
                 timeout: Optional[float]=None):
        """Initializes the game view.
        
        Args:
            game: The game object.
        """

        super().__init__(bot, parent_msg, origin_user, timeout=timeout)

        self.game: GameType = game
