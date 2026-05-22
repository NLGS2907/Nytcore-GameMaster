from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from discord.abc import User

    from ...gamemaster import GameMaster
    from ...games import BaseGame, BaseOptions, EmojisCollection
    from .game_view_base import BaseGameView
    from .options_modal_base import BaseOptionsModal


class GameManager(ABC):
    """Manager that ties the view and model together, and executes the logic."""

    _ignore: bool = False
    games_list: list = []

    def __init_subclass__(cls):
        """Each time a subclass is detected, it gets added here."""

        if hasattr(cls, "_ignore") and cls._ignore:
            return

        __class__.games_list.append(cls)


    def __init__(self, bot: "GameMaster"):
        """Initializes the game object.
        
        Args:
            bot: A reference to the bot user.
        """

        self.bot: "GameMaster" = bot
        self.options: "BaseOptions" = self.options_class()


    @staticmethod
    @abstractmethod
    def game_class() -> type["BaseGame"]:
        """Returns the class of the game object."""

        raise NotImplementedError


    @staticmethod
    @abstractmethod
    def options_class() -> type["BaseOptions"]:
        """Returns the options class of the game."""

        raise NotImplementedError


    @staticmethod
    @abstractmethod
    def view_class() -> type["BaseGameView"]:
        """Returns the view of the game."""

        raise NotImplementedError


    @staticmethod
    @abstractmethod
    def options_modal_class() -> type["BaseOptionsModal"]:
        """Returns the modal class of the game options."""

        raise NotImplementedError


    @property
    def game_title(self) -> str:
        """The title of the underlying game."""

        return self.game_class().title_name()


    @property
    def game_description(self) -> Optional[str]:
        """The optional description of the underlying game."""

        return self.game_class().description()


    @property
    def game_emojis(self) -> "EmojisCollection":
        """Returns a collection of emojis associated with the underlying game."""

        return self.game_class().emojis_collection()


    def assemble_modal(self, timeout: Optional[float]=None) -> "BaseOptionsModal":
        """Creates and loads the modal to modify the options of the game.

        Args:
            timeout: How long to wait (in seconds) until the view is no longer responsive.

        Returns:
            The options modal ready to show.
        """

        return self.options_modal_class(
            self.bot,
            self.options,
            title=self.game_title,
            timeout=timeout
        )


    def assemble_view(self, host: "User", timeout: Optional[float]=None) -> "BaseGameView":
        """Creates and loads the view with all the relevant classes.
        
        Args:
            host: The discord user that started the game.
            timeout: How long to wait (in seconds) until the view is no longer responsive.

        Returns:
            The view, assembled and ready to execute and show.
        """

        return self.view_class(
            self.bot,
            self.game_class(
                self.bot,
                host,
                options=self.options
            ),
            timeout=timeout
        )
