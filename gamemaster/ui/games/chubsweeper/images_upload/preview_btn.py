from typing import TYPE_CHECKING

from discord import ButtonStyle, PartialEmoji
from discord.ui import Button

from .preview_view import ImagePreviewView

if TYPE_CHECKING:
    from discord import Interaction

    from .img_upload_view import ChubMinesUploadView

BLUR_EDIT_EMOJI: str = "🔍"


class ImagePreviewButton(Button):
    """UI button for previewing ChubSweeper images."""

    def __init__(self, parent_view: "ChubMinesUploadView"):
        """Initializes the preview button.
        
        Args:
            parent_view: The parent view from where to fetch the images.
        """

        super().__init__(style=ButtonStyle.blurple,
                         label="Preview",
                         disabled=False,
                         emoji=PartialEmoji.from_str(BLUR_EDIT_EMOJI))
        self.parent_view: "ChubMinesUploadView" = parent_view


    async def callback(self, interaction: "Interaction"):
        async with self.parent_view.lock:
            dealer = self.parent_view.game.dealer
            if not self.parent_view.is_host(interaction.user.id):
                msg_content = (f"{interaction.user.mention}, only **{dealer.username}**, the "
                               f"Dealer, can preview the images.")
                await interaction.response.send_message(msg_content, ephemeral=True)
                return

        safes, mines = self.parent_view.fetch_blurred()
        preview_view = ImagePreviewView(
            self.parent_view.bot,
            self.parent_view.parent_msg,
            self.parent_view.user,
            safes=safes,
            mines=mines
        )
        await preview_view.reset()
        await interaction.response.send_message(files=preview_view.all_images,
                                                view=preview_view, ephemeral=True)
