from abc import ABC, abstractmethod
from traceback import format_exc
from typing import TYPE_CHECKING, Optional

from discord.ui import Modal

from ..logger import DISCORD_NAMESPACE, get_logger

if TYPE_CHECKING:
    from discord import Interaction


class BaseModal(Modal, ABC):
    """Base interface for any common modal."""

    def __init__(self, *, title: str, timeout: Optional[float]=None):
        """Initializes the modal.
        
        Args:
            title: The opening title of the modal.
            timeout: How much time (in seconds) to wait until it no longer
                     receives interactions.
        """

        super().__init__(title=title, timeout=timeout)
        self.prepare()


    @property
    def error_message(self) -> str:
        """Error message to show hen an exception is raised.
        
        This can be inherited to modify the message.
        """

        return "An error has occurred while sending the modal."


    @property
    def success_message(self) -> str:
        """Message to show when the modal is sent successfully.
        
        This can be inherited to modify the message.
        """

        return "Modal processed succesfully."


    def prepare(self):
        """Hook for doing tasks right after initialization.
        
        The default implementation does nothing, but it can be inherited and edited.
        """

        pass


    @abstractmethod
    async def callback(self, interaction: "Interaction"):
        """Callback for executing the logic on submit.
        
        It may also raise exceptions.

        Args:
            interaction: The interaction born from sending the modal.
        """

        raise NotImplementedError


    async def on_error(self, interaction: "Interaction", error: Exception):
        msg_content = (f"**[ERROR]** {self.error_message}\n\n> _{error}_")
        if interaction.response.is_done():
            await interaction.edit_original_response(content=msg_content)
        else:
            await interaction.response.send_message(msg_content, ephemeral=True)
        graceful_err = "\n\t|\t".join(f"Modal has thrown exception {error.__class__!r}:\n"
                                      f"{format_exc()}".split("\n"))
        get_logger(DISCORD_NAMESPACE).error(graceful_err)


    async def on_submit(self, interaction: "Interaction"):
        await self.callback()
        await interaction.response.send_message(f"_{self.success_message}_", ephemeral=True)
