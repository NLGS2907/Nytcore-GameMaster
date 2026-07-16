from typing import TYPE_CHECKING, Optional, TypeAlias

from discord import MediaGalleryItem
from discord.ui import Container, MediaGallery, TextDisplay

from ..base_view import BaseView

if TYPE_CHECKING:
    from discord import File

    from ...gamemaster import GameMaster
    from ..base_view import PossibleMessage, PossibleUser

Files: TypeAlias = list["File"]

GALLERY_MIN_SIZE: int = 1
GALLERY_MAX_SIZE: int = 10


class GalleryView(BaseView):
    """A view for showing images in a chat.

    This is to show gallery in a 'standalone' way.
    """

    def __init__(self,
                 bot: "GameMaster",
                 parent_msg: "PossibleMessage",
                 origin_user: "PossibleUser",
                 *,
                 timeout: Optional[None]=None,
                 title: str="",
                 container: bool=True,
                 images: Files):
        """Initializes the image batch view.

        Aside from those of the parent class, this includes some new arguments.

        Args:
            title: An optional title to show in the view. Leave blank to omit.
            container: Wether to show the gallery inside a container component.
            images: The list of files ready to be sent as images.
        """

        super().__init__(bot, parent_msg, origin_user, timeout=timeout)
        self._title: str = title
        self.__uses_container: bool = container
        self._img: Files = self.validate_img_length(images)


    @staticmethod
    def validate_img_length(files: Files) -> Files:
        """Validates if the given gallery has the correct size.
        
        Raises:
            ValueError: If the gallery size is not in the allowed range.

        Returns:
            The file list as-is, for convenience.
        """

        files_size = len(files)
        if files_size < GALLERY_MIN_SIZE or files_size > GALLERY_MAX_SIZE:
            raise ValueError(f"File list is of size {files_size}. "
                             f"It should be in the range [{GALLERY_MIN_SIZE}, {GALLERY_MAX_SIZE}].")

        return files


    async def reset(self):
        parent_component = (Container() if self.__uses_container else self)

        if self._title:
            parent_component.add_item(TextDisplay(f"### {self._title}"))

        parent_component.add_item(MediaGallery(*(
            MediaGalleryItem(img) for img in self._img
        )))

        if self.__uses_container:
            self.add_item(parent_component)
