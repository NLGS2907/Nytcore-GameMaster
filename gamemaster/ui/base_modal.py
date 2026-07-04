from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from discord.ui import Modal

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


    async def on_submit(self, interaction: "Interaction"):
        try:
            await self.callback()
        except (TypeError, ValueError) as err:
            msg_content = (f"**[ERROR]** {self.error_message}\n\n> _{err}_")
            await interaction.response.send_message(msg_content, ephemeral=True)

            raise err from err

        await interaction.response.send_message(f"_{self.success_message}_", ephemeral=True)
