from typing import TYPE_CHECKING

from discord import ButtonStyle, PartialEmoji
from discord.ui import Button

from .profile_edit_modal import ProfileEditModal

if TYPE_CHECKING:
    from discord import Interaction

    from ...models import Player
    from ...repositories import IPlayerRepository


class EditProfileButton(Button):
    """When clicked it mentions the target Discord user."""

    def __init__(self, player: "Player", player_repository: "IPlayerRepository"):
        """Initializes the button with some references to the parent context.
        
        Args:
            player: The player whose details to edit.
            player_repository: The repository that is used to save the changes.
        """

        super().__init__(style=ButtonStyle.gray,
                         label="Edit Profile",
                         emoji=PartialEmoji.from_str("\u2699"))
        self.player: "Player" = player
        self.player_repository: "IPlayerRepository" = player_repository


    async def callback(self, interaction: "Interaction"):
        await interaction.response.send_modal(ProfileEditModal(self.player, self.player_repository))
