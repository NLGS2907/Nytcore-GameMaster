from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button

if TYPE_CHECKING:
    from discord import Interaction
    from discord.ui import Thumbnail

    from .profile_view import ProfileView


class ShowUserImageButton(Button):
    """Once clicked, it loads and reveals the"""

    def __init__(self, parent_view: "ProfileView", target_thumbnail: "Thumbnail"):
        """Initializes the button with some references to the parent context.
        
        Args:
            parent_view: The parent view from where this button comes from.
            target_thumbnail: The thumbnail that will replace the button.
        """
        super().__init__(style=ButtonStyle.primary,
                         label="Show Image")

        self.parent_view: "ProfileView" = parent_view
        self.target_thumbnail: "Thumbnail" = target_thumbnail


    async def callback(self, interaction: "Interaction"):
        self.parent_view.discord_user_section.accessory = self.target_thumbnail
        await interaction.response.edit_message(view=self.parent_view)

