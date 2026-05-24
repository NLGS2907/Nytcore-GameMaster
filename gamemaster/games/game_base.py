from abc import ABC, abstractmethod
from random import choice
from typing import TYPE_CHECKING, Collection, Generic, Optional, TypeAlias, TypeVar

if TYPE_CHECKING:
    from discord.abc import User

    from ..gamemaster import GameMaster
    from ..models import Player

TitleType: TypeAlias = str
DescriptionType: TypeAlias = str
EmojiType: TypeAlias = str
EmojisCollection: TypeAlias = Collection[EmojiType]
OptionsType = TypeVar("OptionsType")


class BaseGame(Generic[OptionsType], ABC):
    """Base abstract class for a game.
    
    Any game to be created for the bot ought to inherit this.

    Attributes:
        bot: A reference to the bot user.
        host_user: The original user that started the game.
        players: A list of all the players involved in the game.
        options: The options object of this game, if available.
    """

    def __init__(self,
                 bot: "GameMaster",
                 host_user: "User",
                 players: list["Player"],
                 *,
                 options: OptionsType):
        """Initializes the game object.
        
        Args:
            bot: A reference to the bot user.
            host_user: The original user that started the game.
            players: A list of all the players involved in the game.
            options: The options object of this game.
        """

        self.bot: "GameMaster" = bot
        self.host_user: "User" = host_user
        self.players: list["Player"] = players
        self.options: OptionsType = options


    @staticmethod
    @abstractmethod
    def title_name() -> str:
        """The title by which the game will be referenced."""

        raise NotImplementedError


    @staticmethod
    def description() -> Optional[str]:
        """An optional short description for the game.
        
        Set it to `None` to omit it.
        """

        raise None


    @staticmethod
    @abstractmethod
    def emojis_collection() -> EmojisCollection:
        """A set of possible emojis to be associated with this game.
        
        Safe to say, at least one element must be present in this collection.
        """

        raise NotImplementedError


    @classmethod
    def random_emoji(cls) -> EmojiType:
        """Chooses a random emoji from the collection."""

        return choice(cls.emojis_collection())


    @staticmethod
    @abstractmethod
    def minimum_players() -> int:
        """Returns the minimum amount of players allowed in this game."""

        raise NotImplementedError


    @staticmethod
    @abstractmethod
    def maximum_players() -> int:
        """Returns the maximum amount of players allowed in this game."""

        raise NotImplementedError
