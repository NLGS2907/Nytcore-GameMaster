from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button, TextDisplay

if TYPE_CHECKING:
    from discord import Interaction

    from .profile_view import ProfileView


class MentionUserButton(Button):
    """When clicked it mentions the target Discord user."""

    def __init__(self, parent_view: "ProfileView", target_text: str):
        """Initializes the button with some references to the parent context.
        
        Args:
            parent_view: The parent view from where this button comes from.
            target_text: What label to change the button for.
        """

        super().__init__(style=ButtonStyle.primary,
                         label="Mention User")

        self.parent_view: "ProfileView" = parent_view
        self.target_text: str = target_text


    async def callback(self, interaction: "Interaction"):
        self.parent_view.mention_user_component = TextDisplay(self.target_text)

        # can't insert in order, reconstruct from scratch
        self.parent_view.clear_items()
        await self.parent_view.reset()

        await interaction.response.edit_message(view=self.parent_view)
