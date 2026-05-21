from typing import TYPE_CHECKING, Optional, TypeAlias, Union

from discord.ui import LayoutView

if TYPE_CHECKING:
    from discord import InteractionMessage, Member, User

    from ..gamemaster import GameMaster

PossibleUser: TypeAlias = Union["User", "Member"]


class BaseView(LayoutView):
    """Base View for all UIs of the bot."""

    def __init__(self,
                 bot: "GameMaster",
                 parent_msg: "InteractionMessage",
                 origin_user: PossibleUser,
                 *,
                 timeout: Optional[float]=None):
        """Initializes the base view.
        
        Args:
            bot: A reference to the bot user.
            parent_msg: A reference to the parent message that spawned this view.
            origin_user: The orignal user who sent the interaction. The parent message not
                         necessarily holds this information, as the bot is the author most of
                         the time.
            timeout: Timeout, in seconds, from last interaction until the view becomes unresponsive.
        """

        super().__init__(timeout=timeout)

        self.bot: "GameMaster" = bot
        self.parent_msg: "InteractionMessage" = parent_msg
        self.user: PossibleUser = origin_user
