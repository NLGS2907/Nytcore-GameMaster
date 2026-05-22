from typing import TYPE_CHECKING, Optional

from discord.ui import Modal

if TYPE_CHECKING:
    from ...gamemaster import GameMaster


class BaseOptionsModal[OptionsType](Modal):
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

