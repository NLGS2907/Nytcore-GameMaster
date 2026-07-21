from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button

if TYPE_CHECKING:
    from discord import Interaction

    from ..chubsweeper_view import ChubSweeperView


class ReuploadTurnImagesButton(Button):
    """UI Button for the Dealer to reupload images for next turn if necessary."""

    def __init__(self, parent_view: "ChubSweeperView"):
        """Initializes the turn reupload button.
        
        Args:
            parent_view: The parent view of this button.
        """

        super().__init__(style=ButtonStyle.red,
                         label="No, reupload images",
                         disabled=False)
        self.parent_view: "ChubSweeperView" = parent_view


    async def callback(self, interaction: "Interaction"):
        async with self.parent_view.lock:
            dealer = self.parent_view.game.dealer
            if not self.parent_view.is_host(interaction.user.id):
                msg_content = (f"{interaction.user.mention}, only **{dealer.username}**, the "
                               f"Dealer, can reupload images for next turn.")
                await interaction.response.send_message(msg_content, ephemeral=True)
                return

            self.parent_view.update_upload_view()
            self.parent_view.chubmines_upload_view.refresh(interaction)
