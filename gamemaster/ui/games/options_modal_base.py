from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generator, Generic, Optional, TypeVar

from discord.ui import Label

from ..base_modal import BaseModal

if TYPE_CHECKING:
    from discord import Interaction
    from discord.ui import Item

    from ...gamemaster import GameMaster

OptionsType = TypeVar("OptionsType")


class BaseOptionsModal(Generic[OptionsType], BaseModal, ABC):
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

        self.bot: "GameMaster" = bot
        self.options: OptionsType = options

        # so that prepare() can access the options, this goes last
        super().__init__(title=title, timeout=timeout)


    @abstractmethod
    def update_options(self):
        """Updates the underlying options with the selected values."""

        raise NotImplementedError


    def _unpack_components(self) -> Generator[Item[Any]]:
        """Automatically unpacks components inside the labels.

        Yields:
            All the components of the children items of the modal, provided they are labels.
            If the current item is not a label, yield as-is.
        """

        yield from (child for child in self.walk_children() if not isinstance(child, Label))


    @property
    def error_message(self) -> str:
        return "It seems there was an error trying to update the options."


    @property
    def success_message(self) -> str:
        return "Settings updated successfuly."


    async def callback(self, interaction: "Interaction"):
        self.update_options()    
