from typing import TYPE_CHECKING, Optional

from discord.ui import ActionRow, TextDisplay

from ....games import ChubSweeperGame
from ..game_view_base import BaseGameView
from .chubsweeper_start_btn import ChubSweeperStartButton
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

        self.__started: bool = False
        self.__chubsweeper_start_btn: ChubSweeperStartButton = ChubSweeperStartButton(self)


    async def reset(self):
        if not self.__started:
            await self._start_view()
            return

        await self.cancel_game(title="Rest of the game",
                               reason="This section of the game is not made yet.")


    async def _start_view(self):
        """Shows a mini-view for starting the ChubSweeper game."""

        self.__started = True

        self.add_item(TextDisplay(
            f"**{self.game.dealer.username}**, as the Dealer, you will first need to upload "
            "the images that will be used for the rest of this round.\n"
            "Upload them, preview them, and see if they are okay before starting the game."
        ))
        self.add_item(ActionRow(self.__chubsweeper_start_btn))