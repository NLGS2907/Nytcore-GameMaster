from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button

if TYPE_CHECKING:
    from discord import Interaction

    from ...models import DiscordUserIdType
    from .confirmation_view import ConfirmationView


class ReadyButton(Button):
    """Button for editing the game settings in a lobby."""

    def __init__(self, parent_view: "ConfirmationView", player_id: "DiscordUserIdType"):
        """Initializes the settings button.
        
        Args:
            parent_view: The lobby view from where the button originates from.
            player_id: The ID of the player to modify once the button is triggered.
        """

        player_ready = parent_view.is_player_ready(player_id)

        super().__init__(style=(ButtonStyle.green if player_ready else ButtonStyle.blurple),
                         label=("Ready!" if player_ready else "Confirm"),
                         disabled=False)
        self.parent_view: "ConfirmationView" = parent_view
        self.player_id: "DiscordUserIdType" = player_id


    def update(self):
        """Updates the label and color of the button based on the player's avilability."""

        ready = self.parent_view.is_player_ready(self.player_id)
        self.style = (ButtonStyle.green if ready else ButtonStyle.blurple)
        self.label = ("Ready!" if ready else "Confirm")


    async def callback(self, interaction: "Interaction"):
        if not self.player_id == interaction.user.id:
            await interaction.response.send_message(f"{interaction.user.mention}, you are not "
                                                    "the user this button is for. It is for "
                                                    f"<@{self.player_id}>.",
                                                    ephemeral=True)
            return

        async with self.parent_view.lock:
            countdown_running = self.parent_view.countdown.is_running()
            if self.parent_view.is_player_ready(self.player_id):
                self.parent_view.player_not_ready(self.player_id)
                if countdown_running:
                    self.parent_view.countdown.cancel()
            else:
                self.parent_view.player_ready(self.player_id)

            if self.parent_view.all_players_ready() and not countdown_running:
                self.parent_view.countdown.start()

        await self.parent_view.refresh(interaction)