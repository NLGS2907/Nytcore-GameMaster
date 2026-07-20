from itertools import batched
from typing import TYPE_CHECKING, Optional

from discord import File
from discord.ui import ActionRow, TextDisplay

from ....games import PREFERRED_IMG_FORMAT, ChubSweeperGame
from ...batch_sender import BatchImageSender
from ..game_view_base import BaseGameView
from .chubsweeper_start_btn import ChubSweeperStartButton
from .images_upload import ChubMinesUploadView
from .round_gameplay import ImageSelectionButton

if TYPE_CHECKING:
    from io import BytesIO

    from discord import Interaction

    from ....gamemaster import GameMaster
    from ..game_view_base import PossibleMessage, PossibleUser

BUTTONS_PER_ROW: int = 5


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

        self.__started: bool = False
        self.__chubsweeper_start_btn: ChubSweeperStartButton = ChubSweeperStartButton(self)

        self.chubmines_upload_view: ChubMinesUploadView = ChubMinesUploadView(
            self.bot, self.parent_msg, self.user, self.game, parent_view=self, timeout=timeout
        )
        self.batch_sender: Optional[BatchImageSender] = None
        self._img_btns: list[ImageSelectionButton] = []


    async def pre_detach(self):
        content = (f"**[ROUND {self.game.current_round}]** "
                   f"_Showing {len(self.game.current_deck())} images_")
        await self.throw_message(content)


    async def reset(self):
        if not self.__started:
            await self._start_view()
            return

        self.add_item(TextDisplay(
            f"{self.game.current_player.username}, it is your turn.\n"
            f"Choose between these images and see if you land in a ChubMine™."
        ))

        self._regenerate_selection_btns()
        for btn_row in batched(self._img_btns, BUTTONS_PER_ROW):
            self.add_item(ActionRow(*btn_row))


    async def _start_view(self):
        """Shows a mini-view for starting the ChubSweeper game."""

        self.__started = True

        self.add_item(TextDisplay(
            f"**{self.game.dealer.username}**, as the Dealer, you will first need to upload "
            "the images that will be used for the rest of this round.\n"
            "Upload them, preview them, and see if they are okay before starting the game."
        ))
        self.add_item(ActionRow(self.__chubsweeper_start_btn))


    async def start_game(self, interaction: "Interaction"):
        """Initializes the parameters of the game, and sets them to an initial state."""

        await self.throw_message("_Initiating game..._")

        self.game.reset_round()
        await self.reset_selection(interaction)


    async def reset_selection(self, interaction: "Interaction"):
        """Resets the current state of the game inside the same round."""

        await self.show_images(interaction)
        await self.reset()


    @staticmethod
    def convert_to_ds_files(files: list["BytesIO"], name: str="file") -> list[File]:
        """Takes a sequence of attachments, and converts them to their Discord counterparts.

        Args:
            files: The list of files to convert to their library wrappers.
            name: The name prefix to use for each file.
        """

        return [File(file, filename=f"{name}_{i}.{PREFERRED_IMG_FORMAT}")
                for i, file in enumerate(files, start=1)]


    async def _reset_batch_sender(self):
        """Resets the internal batch sender."""

        self.batch_sender = BatchImageSender(
            self.bot, self.parent_msg,
            images=self.convert_to_ds_files(self.game.current_deck()),
            group_size=1,
            container=False
        )


    async def show_images(self, interaction: "Interaction"):
        """Shows the images in many messages if necessary."""

        await self._reset_batch_sender()
        await self.batch_sender.send(interaction, ephemeral=False)


    def _regenerate_selection_btns(self):
        """Generates the selection button list from the internal game deck."""

        self._img_btns.clear()
        for img_choice in self.game.walk_choices():
            self._img_btns.append(ImageSelectionButton(self, img_choice))


    async def renew(self, interaction: "Interaction"):
        """Resets the current state of the view, and detaches it into a new message."""

        await self.reset_selection(interaction)
        await self.refresh(interaction, detach=True)

        # necessarily last, since it only migrates to the new msg after the refresh
        await self.batch_sender.cleanup(include_root=True)


    def make_choice(self, n: int) -> bool:
        """Makes a choice in the underlying game.

        Args:
            n: The index number of the choice.

        Returns:
            A boolean value indicating if the player has lost due to this choice.        
        """

        return self.game.make_choice(n)
