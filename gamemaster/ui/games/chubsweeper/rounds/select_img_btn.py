from typing import TYPE_CHECKING

from discord import ButtonStyle
from discord.ui import Button

if TYPE_CHECKING:
    from discord import Interaction

    from .....games import ImageChoice
    from ..chubsweeper_view import ChubSweeperView


class ImageSelectionButton(Button):
    """UI Button for selecting an image in a ChubSweeper game."""

    def __init__(self, parent_view: "ChubSweeperView", img_choice: "ImageChoice"):
        """Intializes the image selection button.

        Args:
            parent_view: The parent view where the ChubSweeper game is.
            img_choice: The image choice from where to fetch the properties of the button.
        """

        super().__init__(style=self.btn_style(img_choice),
                         label=str(img_choice.number),
                         disabled=img_choice.uncovered)

        self.parent_view: "ChubSweeperView" = parent_view


    @staticmethod
    def btn_style(choice: "ImageChoice") -> ButtonStyle:
        """Determines the button style depending of the given choice status."""

        if not choice.uncovered:
            return ButtonStyle.gray

        if choice.mine:
            return ButtonStyle.red

        return ButtonStyle.green


    async def callback(self, interaction: "Interaction"):
        async with self.parent_view.lock:
            cur_player = self.parent_view.game.current_player
            if cur_player.discord_user_id != interaction.user.id:
                msg_content = (f"{interaction.user.mention}, only the current player "
                               f"(**{cur_player.username}**) may choose now.")
                await interaction.response.send_message(msg_content, ephemeral=True)
                return

            await self.parent_view.make_choice(int(self.label))
            await self.parent_view.renew(interaction)
