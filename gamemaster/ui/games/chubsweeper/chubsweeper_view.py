from itertools import batched
from typing import TYPE_CHECKING, Optional

from discord import File, SeparatorSpacing
from discord.ui import ActionRow, Container, Separator, TextDisplay

from ....games import PREFERRED_IMG_FORMAT, ChubSweeperGame, ImageType
from ...batch_sender import BatchImageSender
from ..game_view_base import BaseGameView
from .chubsweeper_start_btn import ChubSweeperStartButton
from .confirmation import NextConfirmationButton, ReuploadTurnImagesButton
from .images_upload import ChubMinesUploadView
from .rounds import ChubFinishButton, ImageSelectionButton

if TYPE_CHECKING:

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

        self.chubmines_upload_view: ChubMinesUploadView = self._create_upload_view(
            first_time=True, timeout=timeout
        )
        self.batch_sender: Optional[BatchImageSender] = None
        self._img_btns: list[ImageSelectionButton] = []
        self._next_turn_btn: NextConfirmationButton = NextConfirmationButton(
            self, label="Yes, begin next turn"
        )
        self._reupload_img_btn: ReuploadTurnImagesButton = ReuploadTurnImagesButton(self)
        self._next_round_btn: NextConfirmationButton = NextConfirmationButton(
            self, label="Yes, begin next round"
        )
        self._game_end_btn: ChubFinishButton = ChubFinishButton(self)

        self._turn_finished: bool = False
        self._round_finished: bool = False


    async def pre_detach(self):
        content = (f"**[ROUND {self.game.current_round}]** "
                   f"_Showing {len(self.game.current_deck())} images_")
        await self.throw_message(content)


    async def reset(self):
        if not self.__started:
            self._start_view()
            return

        if not self._turn_finished and not self._round_finished:
            self._turn_view()
            return

        cur_score = self.game.current_score()
        container = Container(TextDisplay("## Turn Finished"))
        container.add_item(TextDisplay(
            f"The player **{self.game.current_player.username}** has guessed "
            f"_{cur_score}_ out of _{len(self.game.tracker)}_ possible choices."
            f"\n\n**Final Score:**\t`{cur_score}` points"
        ))
        self.add_item(container)

        if self._round_finished:
            self._round_end_view()
        elif self._turn_finished:
            self._turn_end_view()


    def _create_upload_view(self,
                            *,
                            first_time: bool=True,
                            timeout: Optional[float]=None) -> ChubMinesUploadView:
        """Creates an upload view instance, ready for use.

        Args:
            first_time: Wether we should tell the view this is the first time it is being used.
            timeout: Seconds until the view stops responding to interactions.
        """

        return ChubMinesUploadView(
            self.bot, self.parent_msg, self.user, self.game,
            parent_view=self, first_time=first_time, timeout=timeout
        )


    def _start_view(self):
        """Shows a mini-view for starting the ChubSweeper game."""

        self.__started = True

        self.add_item(TextDisplay(
            f"**{self.game.dealer.username}**, as the Dealer, you will first need to upload "
            "the images that will be used for the rest of this round.\n"
            "Upload them, preview them, and see if they are okay before starting the game."
        ))
        self.add_item(ActionRow(self.__chubsweeper_start_btn))


    def _turn_view(self):
        """Resets the view with the components of a normal turn."""

        cur_score = self.game.current_score()
        self.add_item(TextDisplay(
            f"{self.game.current_player.username}, it is your turn.\n"
            f"Choose between these images and see if you land in a ChubMine™.\n\n"
            f"You have currently guessed correctly a total of **{cur_score}** "
            "times."
        ))

        self._regenerate_selection_btns()
        for btn_row in batched(self._img_btns, BUTTONS_PER_ROW):
            self.add_item(ActionRow(*btn_row))


    def _turn_end_view(self):
        """Modifies the view with the components of the end of a turn."""

        self.add_item(TextDisplay(
            f"Dealer **{self.game.dealer.username}**, do you wish to use the same images "
            "for the next player's turn, or reupload new ones?"
        ))
        self.add_item(ActionRow(self._reupload_img_btn, self._next_turn_btn))


    def _round_end_view(self):
        """Modifies the view with the components of the end of a round."""

        scores = [
            f"**{player.username}**\t`{self.game.get_score(player)}`"
            for player in self.game.miners
        ]
        self.add_item(TextDisplay(
            "That's the end of this round! Here are the current scores:"
            f"\n\n{'\n'.join(scores)}\n\n"
        ))

        winners = self.game.winners()
        winners_names = [f"**{winner.username}**" for winner in winners]

        if len(winners) == 1:
            self.add_item(TextDisplay(
                f"The player **{winners_names[0]}** has more points than most. "
                "_They are the winner!_"
            ))
            self.add_item(TextDisplay(
                f"\nDealer **{self.game.dealer.username}**, you can now end this game."
            ))
            self.add_item(ActionRow(self._game_end_btn))
        else:
            self.add_item(TextDisplay(
                f"The players {', '.join(winners_names)} have tied in score. _We'll have to "
                "do another round to decide the winner..._"
            ))
            self.add_item(TextDisplay(
                f"\nDealer **{self.game.dealer.username}**, do you wish to use the same images "
                "for the next round, or reupload new ones?"
            ))
            self.add_item(ActionRow(self._reupload_img_btn, self._next_round_btn))


    async def finish_view(self):
        """Resets this view to show the ending of the game, and stops any interactions to it.

        The game should have only one winner by this point.
        """

        self.clear_items()
        await self.batch_sender.cleanup(include_root=True)
        winner = self.game.winners()[0]

        container = Container(
            TextDisplay("## ChubSweeper Game Finished"),
            Separator(spacing=SeparatorSpacing.large),

            TextDisplay(
                f"The player **{winner.username}** has won with a score of "
                f"{self.game.get_score(winner)} last round."
            ),

            TextDisplay(
                f"\n-# _Last round had {len(self.game.safes)} safes and "
                f"{len(self.game.mines)} ChubMines™._"
            )
        )
        self.add_item(container)

        await self.refresh_parent_msg()
        self.chubmines_upload_view.stop()
        self.stop()


    async def start_game(self, interaction: "Interaction"):
        """Initializes the parameters of the game, and sets them to an initial state."""

        await self.throw_message("_Initiating game..._")
        await self.reset_game(interaction, first_time=True)


    async def reset_game(self, interaction: "Interaction", *, first_time: bool=False):
        """Resets the state of the game."""

        if self._round_finished:
            self._round_finished = False
            self.game.reset_round()

        if self._turn_finished:
            self._turn_finished = False

        self.game.reset_turn()
        await self.reset_selection(interaction, first_time=first_time)


    async def reset_selection(self, interaction: "Interaction", *, first_time: bool=False):
        """Resets the current state of the game inside the same round."""

        await self.show_images(interaction, first_time=first_time)
        await self.reset()


    def update_upload_view(self):
        """Resets the upload view to a new instance.

        However, it will no longer count as the first time being created.
        """

        self.chubmines_upload_view = self._create_upload_view(first_time=False)


    @staticmethod
    def convert_to_ds_files(files: list[ImageType], name: str="file") -> list[File]:
        """Takes a sequence of attachments, and converts them to their Discord counterparts.

        Args:
            files: The list of files to convert to their library wrappers.
            name: The name prefix to use for each file.

        Returns:
            A list of the library wrappers with the files inside.
        """

        return [
            File(ImageType(file.getvalue()), filename=f"{name}_{i}.{PREFERRED_IMG_FORMAT}")
            for i, file in enumerate(files, start=1)
        ]


    async def _reset_batch_sender(self, *, first_time: bool=False):
        """Resets the internal batch sender."""

        if self.batch_sender is not None:
            await self.batch_sender.cleanup(include_root=not first_time)

        self.batch_sender = BatchImageSender(
            self.bot, self.parent_msg,
            images=self.convert_to_ds_files(self.game.current_deck()),
            group_size=1,
            container=False
        )


    async def show_images(self, interaction: "Interaction", *, first_time: bool=False):
        """Shows the images in many messages if necessary."""

        await self._reset_batch_sender(first_time=first_time)
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


    async def make_choice(self, n: int) -> bool:
        """Makes a choice in the underlying game.

        Args:
            n: The index number of the choice.

        Returns:
            A boolean value indicating if the player has lost due to this choice.        
        """

        if self.game.make_choice(n) or self.game.exhausted_choices():
            self._turn_finished = True

        if self._turn_finished and self.game.last_player():
            self._round_finished = True
