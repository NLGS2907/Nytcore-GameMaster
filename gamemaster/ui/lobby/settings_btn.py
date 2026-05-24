from typing import TYPE_CHECKING

from discord import ButtonStyle, PartialEmoji
from discord.ui import Button

if TYPE_CHECKING:
    from discord import Interaction

    from .lobby_view import LobbyView


class SettingsButton(Button):
    """Button for editing the game settings in a lobby."""

    def __init__(self, parent_view: "LobbyView"):
        """Initializes the settings button.
        
        Args:
            parent_view: The lobby view from where the button originates from.
        """

        super().__init__(style=ButtonStyle.gray,
                         label="Settings",
                         emoji=PartialEmoji.from_str("\u2699"),
                         disabled=False)
        self.parent_view: "LobbyView" = parent_view


    async def callback(self, interaction: "Interaction"):
        if not self.parent_view.is_host(interaction.user):
            await interaction.response.send_message(f"{interaction.user.mention}, only the host "
                                                    "of the lobby may use this button.",
                                                    ephemeral=True)
            return

        await interaction.response.send_modal(self.parent_view.manager.assemble_modal())