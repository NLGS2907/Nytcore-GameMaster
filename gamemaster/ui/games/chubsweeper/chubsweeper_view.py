from typing import TYPE_CHECKING, Optional

from ....games import ChubSweeperGame
from ..game_view_base import BaseGameView
from .images_upload import ChubMinesUploadView

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
        self.chubmines_upload_view: ChubMinesUploadView = ChubMinesUploadView(
            self.bot, self.parent_msg, self.user, self.game, parent_view=self, timeout=timeout
        )


    async def reset(self):
        pass
