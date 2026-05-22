from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generator, Optional, Self, TypeAlias

from ...logger import get_gamemaster_logger

if TYPE_CHECKING:
    from discord import InteractionMessage
    from discord.abc import User

    from ...gamemaster import GameMaster
    from ...games import BaseGame, BaseOptions, EmojisCollection
    from ...models import Player
    from ..base_view import PossibleUser
    from .game_view_base import BaseGameView
    from .options_modal_base import BaseOptionsModal

GameID: TypeAlias = int
GamesMap: TypeAlias = dict[GameID, "GameManager"]


class GameManager(ABC):
    """Manager that ties the view and model together, and executes the logic."""

    _ignore: bool = False
    _games_map: GamesMap = []

    def __init_subclass__(cls):
        """Each time a subclass is detected, it gets added here."""

        if hasattr(cls, "_ignore") and cls._ignore:
            return

        game_id = cls.game_id()
        if game_id in __class__._games_map:
            get_gamemaster_logger().warning(
                f"Game {__class__._games_map[game_id].game_title!r} with ID {game_id} already "
                f"exists. Skipping the addition of game {cls.game_title!r}..."
            )
            return

        __class__._games_map[game_id] = cls


    def __init__(self, bot: "GameMaster"):
        """Initializes the game object.
        
        Args:
            bot: A reference to the bot user.
        """

        self.bot: "GameMaster" = bot
        self.players: set["Player"] = set()
        self.options: "BaseOptions" = self.options_class()


    @staticmethod
    @abstractmethod
    def game_id() -> GameID:
        """Returns the internal ID for the handler of this game.
        
        It must be unique across all game objects, since it is used to retrieve some instances.
        """

        raise NotImplementedError


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


    @classmethod
    def class_with_id(cls, class_id: GameID) -> Optional[type[Self]]:
        """Tries to retrieve one of the subclasses based on its ID.
        
        Args:
            class_id: The ID to search with.

        Returns:
            The manager found, or `None` id it does not exist.
        """

        return cls._games_map.get(class_id)


    @classmethod
    def walk_ids_titles(cls) -> Generator[tuple[GameID, str]]:
        """Iterates through the subclasses to retrieve some of its properties.
        
        Yields:
            A tuple with both the name and the ID of a manager.
        """

        for manager in cls._games_map.values():
            yield manager.game_id(), manager.game_title


    def add_player(self, new_player: "Player"):
        """Adds a new player to the internal collection.
        
        If the player already exists, it does nothing.
        """

        self.players.add(new_player)


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


    def assemble_view(self,
                      host: "User",
                      parent_msg: "InteractionMessage",
                      origin_user: "PossibleUser",
                      *,
                      timeout: Optional[float]=None) -> "BaseGameView":
        """Creates and loads the view with all the relevant classes.
        
        Args:
            host: The discord user that started the game.
            parent_msg: A reference to the parent message that spawned this view.
            origin_user: The orignal user who sent the interaction. The parent message not
                         necessarily holds this information, as the bot is the author most of
                         the time.
            timeout: How long to wait (in seconds) until the view is no longer responsive.

        Returns:
            The view, assembled and ready to execute and show.
        """

        return self.view_class(
            self.bot,
            parent_msg,
            origin_user,
            self.game_class(
                self.bot,
                host,
                list(self.players),
                options=self.options
            ),
            timeout=timeout
        )
