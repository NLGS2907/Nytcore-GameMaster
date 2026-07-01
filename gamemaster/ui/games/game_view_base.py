from typing import TYPE_CHECKING, Generic, Optional, TypeVar

from discord import SeparatorSpacing
from discord.ui import Container, Separator, TextDisplay

from ..base_view import BaseView

if TYPE_CHECKING:
    from discord import Interaction

    from ...gamemaster import GameMaster
    from ..base_view import PossibleMessage, PossibleUser

GameType = TypeVar("GameType")


class BaseGameView(Generic[GameType], BaseView):
    """Base view for a game."""

    def __init__(self,
                 bot: "GameMaster",
                 parent_msg: "PossibleMessage",
                 origin_user: "PossibleUser",
                 game: GameType,
                 *,
                 timeout: Optional[float]=None):
        """Initializes the game view.
        
        Args:
            game: The game object.
        """

        super().__init__(bot, parent_msg, origin_user, timeout=timeout)

        self.game: GameType = game


    async def cancel_game(self, *,
                          title: Optional[str]=None,
                          reason: Optional[str]=None,
                          interaction: Optional["Interaction"]=None):
        """Cancels the game abruptly and without saving.
        
        Args:
            reason: A string denoting the reason as to why it was cancelled.
                    It will be showed to the players in a message.
            interaction: The interaction that triggered the response. If not present,
                         it will try to edit the message as-is.
        """

        self.clear_items()

        msg_title = title or "Game Canceled"
        cancel_reason = reason or "This game seems to have been halted abruptly."

        container = Container(
            TextDisplay(f"## {msg_title}"),
            Separator(spacing=SeparatorSpacing.large),
            TextDisplay("### Reason"),
            TextDisplay(f"_{cancel_reason}_")
        )

        self.add_item(container)
        await self.refresh_parent_msg(interaction)
        self.stop()
