from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button

if TYPE_CHECKING:
    from discord import Interaction

    from .lobby_view import LobbyView


class LeaveButton(Button):
    """Button for joining an open lobby."""

    def __init__(self, parent_view: "LobbyView"):
        """Initializes the leave button.
        
        Args:
            parent_view: The lobby view from where the button originates from.
        """

        super().__init__(style=ButtonStyle.red,
                         label="Leave",
                         disabled=False)
        self.parent_view: "LobbyView" = parent_view


    async def callback(self, interaction: "Interaction"):
        async with self.parent_view.lock:
            ds_user = interaction.user
            if self.parent_view.user == ds_user:
                msg_content = (f"{ds_user.mention}, you are the host of this lobby, and cannot "
                               "leave without destroying the lobby first.")
            elif not self.parent_view.player_present_with_id(ds_user.id):
                msg_content = f"{ds_user.mention}, you never joined this lobby."
            else:
                self.parent_view.remove_player_with_id(ds_user.id)
                await self.parent_view.refresh(interaction)
                return

            await interaction.response.send_message(msg_content, ephemeral=True)