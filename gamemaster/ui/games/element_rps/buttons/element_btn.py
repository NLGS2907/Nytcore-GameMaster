from typing import TYPE_CHECKING, TypeAlias, Union

from discord import ButtonStyle
from discord.ui import Button

if TYPE_CHECKING:
    from discord import Emoji, Interaction, PartialEmoji

    from .....models import ElementType
    from ..element_rps_view import ElementRPSView

PossibleEmoji: TypeAlias = Union["Emoji", "PartialEmoji"]


class ElementButton(Button):
    """Button for editing the game settings in a lobby."""

    def __init__(self,
                 parent_view: "ElementRPSView",
                 element: "ElementType",
                 emoji: PossibleEmoji):
        """Initializes the settings button.
        
        Args:
            parent_view: The lobby view from where the button originates from.
            element: The element type of the button.
            emoji: The emoji to show in the button.
        """

        super().__init__(style=ButtonStyle.gray,
                         emoji=emoji,
                         disabled=False)
        self.parent_view: "ElementRPSView" = parent_view
        self.element: "ElementType" = element


    async def callback(self, interaction: "Interaction"):
        async with self.parent_view.lock:
            if not self.parent_view.game.player_present(interaction.user.id):
                player_1_mention = f"<@{self.parent_view.player_1.discord_user_id}>"
                player_2_mention = f"<@{self.parent_view.player_2.discord_user_id}>"
                msg_content = (f"{interaction.user.mention}, you are not part of this game.\n"
                               f"Only {player_1_mention} and {player_2_mention} may use "
                               "these buttons.")
                await interaction.response.send_message(msg_content, ephemeral=True)
                return

            reveal_running = self.parent_view.reveal.is_running()
            is_player_1 = interaction.user.id == self.parent_view.player_1.discord_user_id
            self.parent_view.game.make_choice(self.element, is_player_1)

            if self.parent_view.game.choices_made() and not reveal_running:
                self.parent_view.reveal.start()

            await self.parent_view.refresh(interaction)