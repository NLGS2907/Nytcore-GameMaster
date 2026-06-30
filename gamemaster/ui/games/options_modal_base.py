from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, Optional, TypeVar

from discord.ui import Modal

if TYPE_CHECKING:
    from discord import Interaction

    from ...gamemaster import GameMaster

OptionsType = TypeVar("OptionsType")


class BaseOptionsModal(Generic[OptionsType], Modal, ABC):
    """Base interface of an options modal."""

    def __init__(self,
                 bot: "GameMaster",
                 options: OptionsType,
                 *,
                 title: str,
                 timeout: Optional[float]=None):
        """Initializes the modal to modify the options.

        Usually called through the lobby, rather than from the game view.
        Besides those of the parent class, this includes a few extra parameters.

        Args:
            bot: A reference to the bot user.
            options: The options to modify.
        """

        super().__init__(title=title, timeout=timeout)

        self.bot: "GameMaster" = bot
        self.options: OptionsType = options
        self.prepare()


    def prepare(self):
        """Hook for doing tasks right after initialization.
        
        The default implementation does nothing, but it can be inherited and edited.
        """

        pass


    @abstractmethod
    def update_options(self):
        """Updates the underlying options with the selected values."""

        raise NotImplementedError


    async def on_submit(self, interaction: "Interaction"):
        try:
            self.update_options()
        except (TypeError, ValueError) as err:
            msg_content = ("**[ERROR]** It seems there was an error trying to update the "
                           f"options.\n\n> _{err}_")
            await interaction.response.send_message(msg_content, ephemeral=True)

            raise err from err

        msg_content = "_Settings updated successfuly_"
        await interaction.response.send_message(msg_content, ephemeral=True)
