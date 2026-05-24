from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button

if TYPE_CHECKING:
    from discord import Interaction

    from .lobby_view import LobbyView


class BeginGameButton(Button):
    """Button for editing the game settings in a lobby."""

    def __init__(self, parent_view: "LobbyView"):
        """Initializes the settings button.
        
        Args:
            parent_view: The lobby view from where the button originates from.
        """

        super().__init__(style=ButtonStyle.green,
                         label="Begin",
                         disabled=False)
        self.parent_view: "LobbyView" = parent_view


    async def callback(self, interaction: "Interaction"):
        if not self.parent_view.is_host(interaction.user):
            await interaction.response.send_message(f"{interaction.user.mention}, only the host "
                                                    "can begin the game.",
                                                    ephemeral=True)
            return

        game_view = self.parent_view.manager.assemble_view(self.parent_view.user,
                                                           self.parent_view.parent_msg,
                                                           interaction.user)
        await interaction.response.edit_message(view=game_view)