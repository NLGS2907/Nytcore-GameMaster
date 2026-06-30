from typing import TYPE_CHECKING, TypeAlias, Union

from discord import ButtonStyle, File, PartialEmoji
from discord.ui import Button

if TYPE_CHECKING:
    from discord import Emoji, Interaction

    from ..element_rps_view import ElementRPSView

PossibleEmoji: TypeAlias = Union["Emoji", PartialEmoji]

ELEMENTS_MAP_PATH: str = "./assets/rps/element_map.png"


class ElementMapButton(Button):
    """Button for showing a help map of the elements in RPS."""

    def __init__(self,
                 parent_view: "ElementRPSView"):
        """Initializes the help button.
        
        Args:
            parent_view: The lobby view from where the button originates from.
        """

        super().__init__(style=ButtonStyle.gray,
                         emoji=PartialEmoji.from_str("\u2754"),
                         label="Help",
                         disabled=False)
        self.parent_view: "ElementRPSView" = parent_view


    async def callback(self, interaction: "Interaction"):
        await interaction.response.send_message(file=File(ELEMENTS_MAP_PATH),
                                                ephemeral=True)
