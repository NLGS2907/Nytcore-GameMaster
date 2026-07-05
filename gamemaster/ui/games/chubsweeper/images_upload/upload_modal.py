from typing import TYPE_CHECKING

from discord.ui import FileUpload, Label

from ....base_modal import BaseModal

if TYPE_CHECKING:
    from discord import Attachment, Interaction

    from .img_upload_view import ChubMinesUploadView

SAFES_MIN: int = 1
SAFES_MAX: int = 7
MINES_MIN: int = 1
MINES_MAX: int = 3

IMG_MIN_SIZE: int = 250
IMG_MAX_SIZE: int = 2500

IMG_DESC_TEMPLATE: str = ("Sizes from {img_min}X{img_min} to {img_max}x{img_max} are allowed, "
                          "and the amount must be in the range [{range_min}, {range_max}]")


class ChubMinesUploadModal(BaseModal):
    """Modal for uploading the images used in a game of ChubSweeper."""

    def __init__(self, parent_view: "ChubMinesUploadView"):
        """Initializes the mines upload modal.
        
        Args:
            parent_view: The mines upload view, to save the images.
        """

        self.parent_view: "ChubMinesUploadView" = parent_view

        super().__init__(title="ChubMines™ Upload", timeout=None)


    @property
    def error_message(self):
        return "There was an error while uploading an image."


    @property
    def success_message(self):
        return "Safes and ChubMines™ updated successfully."


    def prepare(self):
        max_safes = self.parent_view.game.options.amount_safes
        safes_upload = Label(
            text="Safe Images",
            description=IMG_DESC_TEMPLATE.format(img_min=IMG_MIN_SIZE, img_max=IMG_MAX_SIZE,
                                                 range_min=SAFES_MIN, range_max=max_safes),
            component=FileUpload(
                required=True,
                min_values=SAFES_MIN,
                max_values=max_safes,
            )
        )
        self.add_item(safes_upload)

        max_mines = self.parent_view.game.options.amount_mines
        mines_upload = Label(
            text="ChubMines™",
            description=IMG_DESC_TEMPLATE.format(img_min=IMG_MIN_SIZE, img_max=IMG_MAX_SIZE,
                                                 range_min=MINES_MIN, range_max=max_mines),
            component=FileUpload(
                required=True,
                min_values=MINES_MIN,
                max_values=max_mines,
            )
        )
        self.add_item(mines_upload)


    def _validate_attachment(self, attachment: "Attachment", file_type: str="Attachment"):
        """Checks if the given attachment is an image, as is of a proper size.
        
        Args:
            attachment: The attachment to check.
            file_type: A helper string to indicate what kind of file we're dealing with.

        Raises:
            TypeError: If the underlying element does not have an image MIME type.
            ValueError: If the image not within the size range allowed.
        """

        if not self._is_image(attachment):
            raise TypeError(f"{file_type} {attachment.filename!r} does not seem to be an image.")

        if not (IMG_MIN_SIZE <= attachment.width <= IMG_MAX_SIZE
                and IMG_MIN_SIZE <= attachment.height <= IMG_MAX_SIZE):
            raise ValueError(f"{file_type} {attachment.filename!r} has size "
                             f"{attachment.width}x{attachment.height}, which is not in the "
                             f"allowed range [{IMG_MIN_SIZE}x{IMG_MIN_SIZE} - "
                             f"{IMG_MAX_SIZE}x{IMG_MAX_SIZE}]")


    def _validate_images(self, safes: list["Attachment"], mines: list["Attachment"]):
        """Checks if the content type of the given two lists is that of an image, and is of a
        proper size.

        Args:
            safes: The list of safe images.
            mines: The list of ChubMines™.
        
        Raises:
            TypeError: If even one element does not have an image MIME type.
            ValueError: If any image is not within the size range allowed.
        """

        for safe in safes:
            self._validate_attachment(safe, "Safe image")

        for mine in mines:
            self._validate_attachment(mine, "ChubMine")


    async def callback(self, interaction: "Interaction"):
        await interaction.response.defer(ephemeral=True)
        await self.parent_view.switch_processing_flag()

        safes_upload: FileUpload
        mines_upload: FileUpload
        safes_upload, mines_upload = self._unpack_components()
        self._validate_images(safes_upload.values, mines_upload.values)

        if safes_upload.values:
            await self.parent_view.set_safes(safes_upload.values)

        if mines_upload.values:
            await self.parent_view.set_mines(mines_upload.values)

        await self.parent_view.switch_processing_flag()
