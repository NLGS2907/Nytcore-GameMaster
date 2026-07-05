from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button

from .blur_edit_modal import BlurEditModal

if TYPE_CHECKING:
    from discord import Interaction

    from .img_upload_view import ChubMinesUploadView


class BlurEditButton(Button):
    """UI button for editing blur level of ChubSweeper images."""

    def __init__(self, parent_view: "ChubMinesUploadView"):
        """Initializes the blur edit button.
        
        Args:
            parent_view: The parent upload view where the images which to apply the blur are.
        """

        super().__init__(style=ButtonStyle.gray,
                         label="Edit Blur",
                         disabled=False)
        self.parent_view: "ChubMinesUploadView" = parent_view


    async def callback(self, interaction: "Interaction"):
        async with self.parent_view.lock:
            dealer = self.parent_view.game.dealer
            if not self.parent_view.is_host(interaction.user.id):
                msg_content = (f"{interaction.user.mention}, only **{dealer.username}**, the "
                               f"Dealer, can edit the blur of the images.")
                await interaction.response.send_message(msg_content, ephemeral=True)
                return

            await interaction.response.send_modal(BlurEditModal(self.parent_view))
