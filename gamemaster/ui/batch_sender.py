from collections.abc import Coroutine
from itertools import batched
from typing import TYPE_CHECKING, Any, Optional, TypeAlias, Union

from discord import WebhookMessage

from .images import GALLERY_MAX_SIZE, GALLERY_MIN_SIZE, GalleryView

if TYPE_CHECKING:
    from discord import File, Interaction, InteractionCallbackResponse, InteractionMessage

    from ..gamemaster import GameMaster
    from .base_view import PossibleMessage
    from .images import Files

_FilesBatch: TypeAlias = tuple["File", ...]
FileBatches: TypeAlias = tuple[_FilesBatch, ...]

WebHookSender: TypeAlias = Coroutine[Any, Any, WebhookMessage]
InteractionSender: TypeAlias = Coroutine[Any, Any, "InteractionCallbackResponse"]
SenderFunc: TypeAlias = Union[WebHookSender, InteractionSender]
SenderResult: TypeAlias = Union[WebhookMessage, "InteractionCallbackResponse"]
SendableMessage: TypeAlias = Union[WebhookMessage, "InteractionMessage"]

DEFAULT_GROUP_SIZE: int = 1


class BatchImageSender:
    """Utility class to manage multiple Messages.

    This is specially useful when trying to send more files than what the library's limit
    per individual message allows.
    """

    def __init__(self,
                 bot: "GameMaster",
                 *,
                 images: "Files",
                 group_size: int=DEFAULT_GROUP_SIZE,
                 title: str="",
                 container: bool=False):
        """Initializes the batch sender.
        
        Args:
            bot: The Bot user, for convenience purposes.
            images: The image files, already wrapped and ready to send. Unlike other objects that
                    deal with these, its size may be arbitrary.
            group_size: The individual size of every sub-group of images that the global list
                        will be decimated into.
            title: An optional title to show above the galleries. Leave blank to omit.
                   If present and the sender uses more than one gallery, it will only appear
                   aboce the first one.
            container: Wether to encase the elements in a container component or not.
        """

        self.bot: "GameMaster" = bot
        self._images: FileBatches = tuple(batched(images, self.validate_group_size(group_size)))
        self._title: str = title
        self._container: bool = container

        self.__messages: list["PossibleMessage"] = []


    @staticmethod
    def validate_group_size(group_size: int) -> int:
        """Validates if the given group size is correct.
        
        Raises:
            TypeError: If the value specified is not an integer.
            ValueError: If the number is not in the allowed range.

        Returns:
            The group size as-is, for convenience.
        """

        if not isinstance(group_size, int):
            raise TypeError(f"Group size should be an integer. "
                            f"Received type {group_size.__class__}")

        if group_size < GALLERY_MIN_SIZE or group_size > GALLERY_MAX_SIZE:
            raise ValueError(
                f"Group size cannot be {group_size}. "
                f"It should be in the range [{GALLERY_MIN_SIZE}, {GALLERY_MAX_SIZE}]."
            )

        return group_size


    @staticmethod
    def _sender_func(interaction: "Interaction") -> SenderFunc:
        """Decides what function to use to send messages based on the interaction status."""

        return (interaction.followup.send
                if interaction.response.is_done()
                else interaction.response.send_message)


    @staticmethod
    def _extract_msg(sender_result: SenderResult) -> SendableMessage:
        """Extracts the message from the result if needed.

        If the object is already a message, leave as-is.
        """

        if isinstance(sender_result, WebhookMessage):
            return sender_result

        # We assume this is an interaction callback then. Retrieve the resource within
        return sender_result.resource


    def gallery_view(self,
                     *,
                     interaction: "Interaction",
                     title: str="",
                     images: "Files") -> GalleryView:
        """Creates a GalleryView based on the given parameters."""

        return GalleryView(self.bot, None, interaction.user,
                           title=title, container=self._container, images=images)


    async def _send_message(self,
                            interaction: "Interaction",
                            images: "Files",
                            *,
                            title: str="",
                            ephemeral: bool):
        """Sends an individual message.

        Args:
            interaction: The interaction context used to send the messages.
            images: The list of image files to send.
            title: The title to use in the message view.
            ephemeral: Wether the content should only be seen by the originator of the interaction.
        """

        batch_view = self.gallery_view(interaction=interaction, title=title, images=images)
        await batch_view.reset()
        res = await self._sender_func(view=batch_view, files=images, ephemeral=ephemeral)

        msg = self._extract_msg(res)
        batch_view.parent_msg = msg

        self.__messages.append(msg)


    async def send(self, interaction: "Interaction", *, ephemeral: bool=False):
        """Tries to send the internal list of files in a batch of messages.

        Args:
            interaction: The interaction context used to send the messages.
            ephemeral: Wether the content should only be seen by the originator of the interaction.
        """

        first, *rest = self._images
        await self._send_message(interaction, first, title=self._title, ephemeral=ephemeral)

        for img_batch in rest:
            await self._send_message(interaction, img_batch, ephemeral=ephemeral)


    async def cleanup(self, delay: Optional[float]=None):
        """Destroy all messages.

        Args:
            delay: The amount in seconds to wait between each removal.
        """

        for msg in self.__messages:
            await msg.delete(delay=delay)
