from io import BytesIO
from typing import Optional, TYPE_CHECKING

from ..db.datasets import PlayerDataset
from ..models import Player
from .base_repository import BaseRepository

if TYPE_CHECKING:
    from ..models import EmojiType

UNICODE_PREFIX: str = "U+"


class PlayerRepository(BaseRepository):
    @staticmethod
    def dataset_cls():
        return PlayerDataset

    def _model_to_dataset(self, model: Player) -> PlayerDataset:
        return PlayerDataset(id=model._id,
                             username=model.username,
                             discord_id=model.discord_user_id,
                             emoji=(self.emoji_to_unicode(model.emoji)
                                    if model.emoji is not None else model.emoji),
                             profile_img=(model.profile_img.getvalue()
                                          if model.profile_img is not None else model.profile_img))


    def _dataset_to_model(self, dataset: PlayerDataset) -> Player:
        if dataset.profile_img is None:
            img_file = None
        else:
            img_file = BytesIO(dataset.profile_img)
            img_file.seek(0)

        return Player(dataset.get_id(),
                      dataset.username,
                      dataset.discord_id,
                      (dataset.emoji if dataset.emoji is None
                       else self.unicode_to_emoji(dataset.emoji)),
                      img_file)


    def emoji_to_unicode(self, emoji: "EmojiType") -> str:
        """Converts an emoji char into the form 'U+XXXX'.
        
        Args:
            emoji: The emoji to convert. It is assumed the emoji is composed of only one character.

        Returns:
            The parsed string, ready to be stored.
        """

        return f"{UNICODE_PREFIX}{ord(emoji):X}"


    def unicode_to_emoji(self, unicode_str: str) -> "EmojiType":
        """Converts a string of form 'U+XXXX' to an emoji char.

        Args:
            unicode_str: The string to parse.

        Returns:
            A raw emoji char.
        """

        prefix_len = len(UNICODE_PREFIX)
        hex_base = 16
        return chr(int(unicode_str[prefix_len:], hex_base))


    def create(self,
               username: str,
               discord_user_id: int,
               emoji: Optional[str]=None,
               profile_img: Optional["BytesIO"]=None) -> Player:
        """Creates a new player, or retrieves it if it already exists.
        
        Args:
            username: The name of the player.
            discord_user_id: The discord user ID tied to the player.
            emoji: An optional emoji to be used in some minigames.
            profile_img: The custom profile image that the player chose.
        """

        validated_username = Player.validate_name(username)
        validated_emoji = Player.validate_emoji(emoji)
        validated_img = Player.validate_profile_img(profile_img)
        validated_img_data = (validated_img.getvalue() if validated_img is not None else None)

        result = self._create_dataset(dict(username=validated_username,
                                           discord_id=discord_user_id,
                                           emoji=validated_emoji,
                                           profile_img=validated_img_data),
                                      get_args=dict(discord_id=discord_user_id))

        return self._dataset_to_model(result)


    def get_by_discord_id(self, discord_id: int) -> Optional[Player]:
        """Tries to retrieve a player based on its discord user ID.

        Args:
            discord_id: The discord user's ID to use.

        Returns:
            A player object if found, `None` if not.
        """

        dataset = self.dataset_cls().get_or_none(self.dataset_cls().discord_id == discord_id)
        return (dataset if dataset is None else self._dataset_to_model(dataset))
