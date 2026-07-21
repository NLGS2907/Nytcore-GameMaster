from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button

if TYPE_CHECKING:
    from discord import Interaction

    from ..chubsweeper_view import ChubSweeperView


class NextTurnConfirmationButton(Button):
    """UI Button for the Dealer to confirm to proceed to the next player in the round."""

    def __init__(self, parent_view: "ChubSweeperView"):
        """Initializes the next turn button.
        
        Args:
            parent_view: The parent view of this button.
        """

        super().__init__(style=ButtonStyle.green,
                         label="Yes, begin next turn",
                         disabled=False)
        self.parent_view: "ChubSweeperView" = parent_view


    async def callback(self, interaction: "Interaction"):
        async with self.parent_view.lock:
            dealer = self.parent_view.game.dealer
            if not self.parent_view.is_host(interaction.user.id):
                msg_content = (f"{interaction.user.mention}, only **{dealer.username}**, the "
                               f"Dealer, can begin the next turn.")
                await interaction.response.send_message(msg_content, ephemeral=True)
                return

            await self.parent_view.reset_game(interaction)
            await self.parent_view.refresh(interaction, detach=True)