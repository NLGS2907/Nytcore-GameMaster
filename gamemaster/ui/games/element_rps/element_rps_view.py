from typing import TYPE_CHECKING, Optional

from ....games import ElementRPSGame
from ..game_view_base import BaseGameView

if TYPE_CHECKING:
    from ....gamemaster import GameMaster
    from ..game_view_base import PossibleMessage, PossibleUser


class ElementRPSView(BaseGameView[ElementRPSGame]):
    """Game view for Element Rock-Paper-Scissors."""

    def __init__(self,
                 bot: "GameMaster",
                 parent_msg: "PossibleMessage",
                 origin_user: "PossibleUser",
                 game: ElementRPSGame,
                 *,
                 timeout: Optional[float]=None):
        super().__init__(bot, parent_msg, origin_user, game, timeout=timeout)

        
