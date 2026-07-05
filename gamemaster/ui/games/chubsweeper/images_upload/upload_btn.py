from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button

from .upload_modal import ChubMinesUploadModal

if TYPE_CHECKING:
    from discord import Interaction

    from .img_upload_view import ChubMinesUploadView


class ImagesUploadButton(Button):
    """UI button for uploading images to the view."""

    def __init__(self, parent_view: "ChubMinesUploadView", title: str):
        """Initializes the upload button.
        
        Args:
            parent_view: The parent upload view, which to save the images into.
            title: The content of the button text.
        """

        super().__init__(style=ButtonStyle.blurple,
                         label=title,
                         disabled=False)
        self.parent_view: "ChubMinesUploadView" = parent_view


    async def callback(self, interaction: "Interaction"):
        async with self.parent_view.lock:
            dealer = self.parent_view.game.dealer
            if not self.parent_view.is_host(interaction.user.id):
                msg_content = (f"{interaction.user.mention}, only **{dealer.username}**, the "
                               f"Dealer, can upload images for this game.")
                await interaction.response.send_message(msg_content, ephemeral=True)
                return

            await interaction.response.send_modal(ChubMinesUploadModal(self.parent_view))
