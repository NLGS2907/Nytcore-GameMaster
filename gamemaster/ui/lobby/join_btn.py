from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button

if TYPE_CHECKING:
    from discord import Interaction

    from .lobby_view import LobbyView


class JoinButton(Button):
    """Button for joining an open lobby."""

    def __init__(self, parent_view: "LobbyView"):
        """Initializes the join button.
        
        Args:
            parent_view: The lobby view from where the button originates from.
        """

        super().__init__(style=ButtonStyle.green,
                         label="Join",
                         disabled=False)
        self.parent_view: "LobbyView" = parent_view


    async def callback(self, interaction: "Interaction"):
        async with self.parent_view.lock:
            ds_user = interaction.user
            if self.parent_view.player_present_with_id(ds_user.id):
                msg_content = f"{ds_user.mention}, you already joined this lobby."
            elif self.parent_view.players_full():
                msg_content = (f"{ds_user.mention}, you cannot join this lobby, as "
                               "it is already full.")
            else:
                self.parent_view.add_player(self.parent_view.player_from_user(ds_user))
                await self.parent_view.refresh(interaction)
                return
                
            await interaction.response.send_message(msg_content, ephemeral=True)
