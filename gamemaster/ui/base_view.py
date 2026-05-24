from asyncio import Lock
from typing import TYPE_CHECKING, Optional, TypeAlias, Union

from discord.ui import LayoutView

if TYPE_CHECKING:
    from discord import Interaction, InteractionMessage, Member, Message, User

    from ..gamemaster import GameMaster

PossibleUser: TypeAlias = Union["User", "Member"]
PossibleMessage: TypeAlias = Union["Message", "InteractionMessage"]


class BaseView(LayoutView):
    """Base View for all UIs of the bot.
    
    Attributes:
        bot: A reference to the bot user.
        parent_msg: A reference to the parent message that spawned this view.
        user: The orignal user who sent the interaction. The parent message not necessarily holds
              this information, as the bot is the author most of the time.
        lock: A Lock for managing shared resources in asyncio tasks.
    """

    def __init__(self,
                 bot: "GameMaster",
                 parent_msg: PossibleMessage,
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
        self.lock: Lock = Lock()


    async def refresh_parent_msg(self, interaction: Optional["Interaction"]=None):
        """Refreshes the message that contains the view.
        
        Args:
            interaction: The interaction that triggered the response. If not present, it will try
                         to edit the message as-is.
        """

        if interaction is not None and not interaction.response.is_done():
            await interaction.response.edit_message(view=self)
            return

        await self.parent_msg.edit(view=self)
