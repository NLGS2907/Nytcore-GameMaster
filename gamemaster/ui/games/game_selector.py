from typing import TYPE_CHECKING, Optional

from discord import SeparatorSpacing
from discord.ui import ActionRow, Container, Separator, TextDisplay

from .selector_menu import GameSelectionMenu

if TYPE_CHECKING:
    from discord import InteractionMessage

    from ...gamemaster import GameMaster
    from ..base_view import PossibleUser

from ..base_view import BaseView


class GameSelectorView(BaseView):
    """View for selecting games in a more detailed way."""

    def __init__(self,
                 bot: "GameMaster",
                 parent_msg: "InteractionMessage",
                 origin_user: "PossibleUser",
                 *,
                 timeout: Optional[float]=None):
        super().__init__(bot, parent_msg, origin_user, timeout=timeout)

        self.container: Container = Container(
            TextDisplay("## Game Selector"),
            Separator(visible=True, spacing=SeparatorSpacing.small)
        )
        self.selector: GameSelectionMenu = GameSelectionMenu()
        self.container.add_item(ActionRow(self.selector))

        self.add_item(self.container)
