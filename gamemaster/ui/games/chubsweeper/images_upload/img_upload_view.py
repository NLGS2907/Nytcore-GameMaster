from io import BytesIO
from typing import TYPE_CHECKING, Optional

from discord import File, SeparatorSpacing
from discord.ui import ActionRow, Container, Separator, TextDisplay

from .....games import ChubSweeperGame
from ...game_view_base import BaseGameView
from .blur_edit_btn import BlurEditButton
from .preview_btn import ImagePreviewButton
from .round_begin_btn import RoundBeginButton
from .upload_btn import ImagesUploadButton

if TYPE_CHECKING:
    from discord import Attachment

    from .....gamemaster import GameMaster
    from .....games import BlurLevel
    from ...game_view_base import PossibleMessage, PossibleUser
    from ..chubsweeper_view import ChubSweeperView

NOT_UPLOADED_TEMPLATE: str = "❌ No {img_type} uploaded yet"
UPLOADED_TEMPLATE: str = "✅ **{img_type} successfully loaded:**\t{amount}"


class ChubMinesUploadView(BaseGameView[ChubSweeperGame]):
    """Mini view for Chubsweeper's stage of uploading images."""

    def __init__(self,
                 bot: "GameMaster",
                 parent_msg: "PossibleMessage",
                 origin_user: "PossibleUser",
                 game: ChubSweeperGame,
                 *,
                 parent_view: "ChubSweeperView",
                 timeout: Optional[float]=None):
        super().__init__(bot, parent_msg, origin_user, game, timeout=timeout)
        self.chubsweeper_view: "ChubSweeperView" = parent_view
        self._safes: list["Attachment"] = []
        self._mines: list["Attachment"] = []
        self.__processing: bool = False

        self._upload_btn: ImagesUploadButton = ImagesUploadButton(self, "Upload Images")
        self._blur_edit_btn: BlurEditButton = BlurEditButton(self)
        self._preview_btn: ImagePreviewButton = ImagePreviewButton(self)
        self._round_begin_btn: RoundBeginButton = RoundBeginButton(self, self.chubsweeper_view)


    def _not_uploaded_yet(self) -> bool:
        """Checks if nothing was uploaded at all."""

        return not self._safes and not self._mines


    async def switch_processing_flag(self, refresh: bool=True):
        """Switches the internal flag for internal image processing.
        
        Args:
            refresh: Wether to additionally refresh the parent view.
        """

        self.__processing = not self.__processing
        if refresh:
            await self.refresh()


    async def reset(self):
        nothing_uploaded = self._not_uploaded_yet()
        chubmines = "ChubMines™"
        safes = "Safes"

        container = Container(
            TextDisplay("## ChubSweeper Images Upload"),
            Separator(spacing=SeparatorSpacing.large)
        )

        status_msg = ((f"**{self.game.dealer.username}**, as the dealer, you must upload the "
                       f"safe images as well as the {chubmines} to be used in the next rounds.")
                      if not self.__processing else "_Processing images..._")
        container.add_item(TextDisplay(status_msg))
        container.add_item(Separator(spacing=SeparatorSpacing.small))

        if self.__processing:
            container.add_item(TextDisplay(
                "-# **Please note** that uploading the images may take a few seconds."
            ))
        else:
            container.add_item(TextDisplay(
                NOT_UPLOADED_TEMPLATE.format(img_type=safes)
                if nothing_uploaded
                else UPLOADED_TEMPLATE.format(img_type=safes, amount=len(self._safes))
            ))
            container.add_item(TextDisplay(
                NOT_UPLOADED_TEMPLATE.format(img_type=chubmines)
                if nothing_uploaded
                else UPLOADED_TEMPLATE.format(img_type=chubmines, amount=len(self._mines))
            ))
            container.add_item(Separator(spacing=SeparatorSpacing.small))

            self._upload_btn.label = ("Upload ChubMines™"
                                    if nothing_uploaded
                                    else "Reupload ChubMines™")
            img_buttons = ActionRow(self._upload_btn)
            if not nothing_uploaded:
                img_buttons.add_item(self._blur_edit_btn)

            container.add_item(img_buttons)

            if not nothing_uploaded:
                container.add_item(ActionRow(self._preview_btn, self._round_begin_btn))

        self.add_item(container)


    @staticmethod
    async def _attachment_to_file(attachment: "Attachment") -> BytesIO:
        """Transforms a Discord attachment into a in-memory binary file."""

        file = BytesIO()
        await attachment.save(file, seek_begin=True)

        return file


    async def set_safes(self, safes: list["Attachment"]):
        """Sets the attachment sfor the safe images."""

        self._safes = safes
        self.game.set_safes([await self._attachment_to_file(safe) for safe in self._safes])


    async def set_mines(self, mines: list["Attachment"]):
        """Sets the attachment sfor the ChubMines™."""

        self._mines = mines
        self.game.set_mines([await self._attachment_to_file(mine) for mine in self._mines])


    def reblur_images(self, blur_level: "BlurLevel"):
        """Tries to reblur the images of the ChubSweeper game.
        
        Args:
            blur_level: The new obfuscation intensity.
        """

        self.game.reblur_images(blur_level)


    def fetch_blurred(self) -> tuple[list[File], list[File]]:
        """Returns a tuple with the blurred versions of both list of images."""

        return (self.chubsweeper_view.convert_to_ds_files(self.game.safes_blurred(), "safe"),
                self.chubsweeper_view.convert_to_ds_files(self.game.mines_blurred(), "chubmine"))
