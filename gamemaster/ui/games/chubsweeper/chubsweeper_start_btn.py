from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button

if TYPE_CHECKING:
    from discord import Interaction

    from .chubsweeper_view import ChubSweeperView


class ChubSweeperStartButton(Button):
    """UI button for starting a game of ChubSweeper."""

    def __init__(self, parent_view: "ChubSweeperView"):
        """Initializes the start button.
        
        Args:
            parent_view: The parent game view.
        """

        super().__init__(style=ButtonStyle.green,
                         label="Start",
                         disabled=False)
        self.parent_view: "ChubSweeperView" = parent_view


    async def callback(self, interaction: "Interaction"):
        async with self.parent_view.lock:
            dealer = self.parent_view.game.dealer
            if not self.parent_view.is_host(interaction.user.id):
                msg_content = (f"{interaction.user.mention}, only **{dealer.username}**, the "
                               f"Dealer, can start this process.")
                await interaction.response.send_message(msg_content, ephemeral=True)
                return

            await self.parent_view.chubmines_upload_view.reset()
            await self.parent_view.refresh_parent_msg(interaction,
                                                      self.parent_view.chubmines_upload_view)
