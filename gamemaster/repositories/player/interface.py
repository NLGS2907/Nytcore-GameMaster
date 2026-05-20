"""Interface for player repositories."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from ..base_repository import BaseRepository

if TYPE_CHECKING:
    from io import BytesIO

    from ...models import EmojiType, Player


class IPlayerRepository(BaseRepository, ABC):
    """Interface for player repositories.
    
    Any repository that wants to deal with players' data must implement these interface.
    """

    @abstractmethod
    def emoji_to_unicode(self, emoji: "EmojiType") -> str:
        """Converts an emoji char into the form 'U+XXXX'.
        
        Args:
            emoji: The emoji to convert. It is assumed the emoji is composed of only one character.

        Returns:
            The parsed string, ready to be stored.
        """

        raise NotImplementedError


    @abstractmethod
    def unicode_to_emoji(self, unicode_str: str) -> "EmojiType":
        """Converts a string of form 'U+XXXX' to an emoji char.

        Args:
            unicode_str: The string to parse.

        Returns:
            A raw emoji char.
        """

        raise NotImplementedError


    @abstractmethod
    def create(self,
               username: str,
               discord_user_id: int,
               emoji: Optional[str]=None,
               profile_img: Optional["BytesIO"]=None) -> "Player":
        """Creates a new player, or retrieves it if it already exists.
        
        Args:
            username: The name of the player.
            discord_user_id: The discord user ID tied to the player.
            emoji: An optional emoji to be used in some minigames.
            profile_img: The custom profile image that the player chose.
        """

        raise NotImplementedError


    @abstractmethod
    def get_by_discord_id(self, discord_id: int) -> Optional["Player"]:
        """Tries to retrieve a player based on its discord user ID.

        Args:
            discord_id: The discord user's ID to use.

        Returns:
            A player object if found, `None` if not.
        """

        raise NotImplementedError
