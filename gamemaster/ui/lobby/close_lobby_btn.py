from typing import TYPE_CHECKING

from discord import ButtonStyle, PartialEmoji
from discord.ui import Button

from ..throwable_view import ThrowableView

if TYPE_CHECKING:
    from discord import Interaction

    from .lobby_view import LobbyView


class CloseLobbyButton(Button):
    """Button for editing the game settings in a lobby."""

    def __init__(self, parent_view: "LobbyView"):
        """Initializes the settings button.
        
        Args:
            parent_view: The lobby view from where the button originates from.
        """

        super().__init__(style=ButtonStyle.red,
                         label="Close Lobby",
                         emoji=PartialEmoji.from_str("\u2716"),
                         disabled=False)
        self.parent_view: "LobbyView" = parent_view


    async def callback(self, interaction: "Interaction"):
        if not self.parent_view.is_host(interaction.user):
            await interaction.response.send_message(f"{interaction.user.mention}, only the host "
                                                    "may close the lobby.",
                                                    ephemeral=True)
            return

        msg_content = "_The host of this lobby has decided to close the session._"
        await interaction.response.edit_message(view=ThrowableView(msg_content))