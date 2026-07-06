from io import BytesIO
from typing import TYPE_CHECKING, Optional

from discord import File, MediaGalleryItem, SeparatorSpacing
from discord.ui import Container, MediaGallery, Separator, TextDisplay

from .....games import PREFERRED_IMG_FORMAT
from ....base_view import BaseView

if TYPE_CHECKING:
    from .....gamemaster import GameMaster
    from ....base_view import PossibleMessage, PossibleUser


class ImagePreviewView(BaseView):
    """UI view for showing the uploaded images."""

    def __init__(self,
                 bot: "GameMaster",
                 parent_msg: "PossibleMessage",
                 origin_user: "PossibleUser",
                 *,
                 safes: list[BytesIO],
                 mines: list[BytesIO],
                 timeout: Optional[float]=None):
        """Initializes the base view.
        
        Args:
            bot: A reference to the bot user.
            parent_msg: A reference to the parent message that spawned this view.
            origin_user: The orignal user who sent the interaction. The parent message not
                         necessarily holds this information, as the bot is the author most of
                         the time.
            safes: The safe images to use for showing.
            mines: The ChubMines to use for showing.
            timeout: Timeout, in seconds, from last interaction until the view becomes unresponsive.
        """

        super().__init__(bot, parent_msg, origin_user, timeout=timeout)
        self.safes: list[File] = self._convert_to_ds_files(safes, "safe")
        self.mines: list[File] = self._convert_to_ds_files(mines, "chubmine")


    @property
    def all_images(self) -> list[File]:
        """Retrieves both the safe images and the ChubMines."""

        return self.safes + self.mines


    @staticmethod
    def _file_to_ds_file(file: BytesIO) -> File:
        """Converts a binary file into the Discord wrapper."""

        file_pos = file.tell()
        file_data = file.getvalue()

        copied_file = BytesIO(file_data)
        copied_file.seek(file_pos)

        return File(copied_file)


    @staticmethod
    def _convert_to_ds_files(file_list: list[BytesIO], name: str="file") -> list[File]:
        """Takes a sequence of binary files, and converts them to their Discord counterparts."""

        return [File(file, filename=f"{name}_{i}.{PREFERRED_IMG_FORMAT}")
                for i, file in enumerate(file_list, start=1)]


    async def reset(self):
        container = Container(
            TextDisplay("## ChubMines Preview"),
            Separator(spacing=SeparatorSpacing.large)
        )

        container.add_item(TextDisplay("### Safes"))
        container.add_item(MediaGallery(*(
            MediaGalleryItem(media=safe)
            for safe in self.safes
        )))

        container.add_item(TextDisplay("### ChubMines™"))
        container.add_item(MediaGallery(*(
            MediaGalleryItem(media=mine)
            for mine in self.mines
        )))

        self.add_item(container)
