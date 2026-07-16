from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button

if TYPE_CHECKING:
    from discord import Interaction

    from ..chubsweeper_view import ChubSweeperView
    from .img_upload_view import ChubMinesUploadView


class RoundBeginButton(Button):
    """UI button for beginning a round of ChubSweeper."""

    def __init__(self, parent_view: "ChubMinesUploadView", target_view: "ChubSweeperView"):
        """Initializes the round begin button.
        
        Args:
            parent_view: The parent view where this button lives.
            target_view: The view to return to.
        """

        super().__init__(style=ButtonStyle.green,
                         label="Begin Round",
                         disabled=False)
        self.parent_view: "ChubMinesUploadView" = parent_view
        self.target_view: "ChubSweeperView" = target_view


    async def callback(self, interaction: "Interaction"):
        async with self.parent_view.lock:
            dealer = self.parent_view.game.dealer
            if not self.parent_view.is_host(interaction.user.id):
                msg_content = (f"{interaction.user.mention}, only **{dealer.username}**, the "
                               f"Dealer, can make the call to begin the round.")
                await interaction.response.send_message(msg_content, ephemeral=True)
                return

            await interaction.response.defer()
            self.parent_view.stop()

            await self.target_view.start_game(interaction)
            await self.target_view.refresh(interaction, detach=True)
