from asyncio import Lock
from traceback import format_exc
from typing import TYPE_CHECKING, Optional, Self, TypeAlias, Union

from discord.ui import LayoutView

from .throwable_view import ThrowableView

if TYPE_CHECKING:
    from discord import Interaction, InteractionMessage, Member, Message, User
    from discord.ui import Item

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
        self.parent_msg: PossibleMessage = parent_msg
        self.user: PossibleUser = origin_user
        self.lock: Lock = Lock()


    async def on_error(self,
                       interaction: "Interaction",
                       error: Exception,
                       item: Item):
        """Default error message handler for exceptions.

        Args:
            interaction: The discord interaction from which the error originated.
            error: An instance of the error itself.
            item: The UI item from where the error originated.
        """

        error_msg = "\n".join(f"> _{line.replace('_', r'\_')}_" for line in str(error).split("\n"))
        msg_content = f"**[ERROR]** Looks like an error has ocurred.\n\n{error_msg}"
        error_view = ThrowableView(msg_content)
        if interaction.response.is_done():
            await interaction.edit_original_response(view=error_view)
        else:
            await interaction.response.send_message(view=error_view, ephemeral=True)
        graceful_err = "\n\t|\t".join(f"Item {item!r} has thrown exception {error.__class__!r} "
                                      f"from view {item.view!r}:\n{format_exc()}".split("\n"))
        self.bot.log.error(graceful_err)


    async def reset(self):
        """Resets the view, refreshing all of its elements.

        Note that if you call this directly, it will NOT wipe out the prior components, you must
        do that yourself with `clear_items()` or by using `refresh()`.

        The default implementations does nothing, but can be inherited to be changed.
        """

        pass


    async def refresh_parent_msg(self,
                                 interaction: Optional["Interaction"]=None,
                                 view: Optional[Self]=None):
        """Refreshes the message that contains the view.
        
        Args:
            interaction: The interaction that triggered the response. If not present, it will try
                         to edit the message as-is.
            view: The view to refresh the message with. If not specified, it will use this
                  very instance.
        """

        usable_view = view or self

        if interaction is not None and not interaction.response.is_done():
            await interaction.response.edit_message(view=usable_view)
            return

        await self.parent_msg.edit(view=usable_view)


    async def refresh(self, interaction: Optional["Interaction"]=None):
        """Refreshes the elements of this view, then the message itself.
        
        Args:
            interaction: The interaction that triggered the response. If not present, it will try
                         to edit the message as-is.
        """

        self.clear_items()
        await self.reset()
        await self.refresh_parent_msg(interaction)


    async def destroy(self, interaction: Optional["Interaction"]=None):
        """Deletes the original message where this view lives.

        Args:
            interaction: If present, it will fetch the original message this way.
        """

        if interaction is not None:
            await interaction.delete_original_response()
            return

        await self.parent_msg.delete()

