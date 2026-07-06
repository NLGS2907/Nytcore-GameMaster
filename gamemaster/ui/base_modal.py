from abc import ABC, abstractmethod
from traceback import format_exc
from typing import TYPE_CHECKING, Any, Generator, Optional

from discord import InteractionResponseType
from discord.ui import Item, Label, Modal

from ..logger import DISCORD_NAMESPACE, get_logger

if TYPE_CHECKING:
    from discord import Attachment, Interaction, InteractionResponse


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


    def _unpack_components(self) -> Generator[Item[Any]]:
        """Automatically unpacks components inside the labels.

        Yields:
            All the components of the children items of the modal, provided they are labels.
            If the current item is not a label, yield as-is.
        """

        yield from (child for child in self.walk_children() if not isinstance(child, Label))


    def _is_image(self, attachment: "Attachment") -> bool:
        """Determines if the given attachment is that of an image."""

        return "image" in attachment.content_type


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


    def _response_was_deferred(self, response: "InteractionResponse") -> bool:
        """Checks if the given response was done due to being deferred."""

        return response.type in (
            InteractionResponseType.deferred_channel_message,
            InteractionResponseType.deferred_message_update
        )


    async def _send_message(self, interaction: "Interaction", *, content: str, ephemeral: bool=False):
        """Sends a message while being aware of the interaction state.
        
        Args:
            interaction: The interaction from which to get the context.
            content: The content of the message.
            ephemeral: Wether the message should only appear to the originator of the interaciton.
        """

        if not interaction.response.is_done():
            await interaction.response.send_message(content, ephemeral=ephemeral)
        elif self._response_was_deferred(interaction.response):
            # in practice, the message is only truly ephemeral if the value declared is the same
            # as that of `defer()`
            await interaction.followup.send(content, ephemeral=ephemeral)
        else:
            await interaction.edit_original_response(content)


    async def on_error(self, interaction: "Interaction", error: Exception):
        error_msg = "\n".join(f"> _{line}_" for line in str(error).split("\n"))
        msg_content = (f"**[ERROR]** {self.error_message}\n\n{error_msg}")
        await self._send_message(interaction, content=msg_content, ephemeral=True)

        graceful_err = "\n\t|\t".join(f"Modal has thrown exception {error.__class__!r}:\n"
                                      f"{format_exc()}".split("\n"))
        get_logger(DISCORD_NAMESPACE).error(graceful_err)


    async def on_submit(self, interaction: "Interaction"):
        await self.callback(interaction)
        await self._send_message(interaction, content=f"_{self.success_message}_", ephemeral=True)
