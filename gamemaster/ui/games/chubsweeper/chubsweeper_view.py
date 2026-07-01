from typing import TYPE_CHECKING, Optional

from ....games import ChubSweeperGame
from ..game_view_base import BaseGameView

if TYPE_CHECKING:
    from ....gamemaster import GameMaster
    from ..game_view_base import PossibleMessage, PossibleUser


class ChubSweeperView(BaseGameView[ChubSweeperGame]):
    """Game view for ChubSweeper."""

    def __init__(self,
                 bot: "GameMaster",
                 parent_msg: "PossibleMessage",
                 origin_user: "PossibleUser",
                 game: ChubSweeperGame,
                 *,
                 timeout: Optional[float]=None):
        super().__init__(bot, parent_msg, origin_user, game, timeout=timeout)