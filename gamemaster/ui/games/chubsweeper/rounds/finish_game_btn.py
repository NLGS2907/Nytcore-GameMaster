from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button

if TYPE_CHECKING:
    from discord import Interaction

    from ..chubsweeper_view import ChubSweeperView


class ChubFinishButton(Button):
    """UI Button for ending a ChubSweeper game."""

    def __init__(self, parent_view: "ChubSweeperView"):
        """Intializes the image selection button.

        Args:
            parent_view: The parent view where the ChubSweeper game is.
        """

        super().__init__(style=ButtonStyle.green,
                         label="End Game",
                         disabled=False)

        self.parent_view: "ChubSweeperView" = parent_view


    async def callback(self, interaction: "Interaction"):
        async with self.parent_view.lock:
            dealer = self.parent_view.game.dealer
            if not self.parent_view.is_host(interaction.user.id):
                msg_content = (f"{interaction.user.mention}, only **{dealer.username}**, the "
                               f"Dealer, may formally end the game.")
                await interaction.response.send_message(msg_content, ephemeral=True)
                return

            await self.parent_view.finish_view()
