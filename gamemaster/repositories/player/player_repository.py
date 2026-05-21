from io import BytesIO
from typing import Optional, TYPE_CHECKING

from ...db.datasets import PlayerDataset
from ...models import Player
from .interface import IPlayerRepository

if TYPE_CHECKING:
    from ...models import EmojiType

UNICODE_PREFIX: str = "U+"


class PlayerRepository(IPlayerRepository):
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
        return f"{UNICODE_PREFIX}{ord(emoji):X}"


    def unicode_to_emoji(self, unicode_str: str) -> "EmojiType":
        prefix_len = len(UNICODE_PREFIX)
        hex_base = 16
        return chr(int(unicode_str[prefix_len:], hex_base))


    def create(self,
               username: str,
               discord_user_id: int,
               emoji: Optional[str]=None,
               profile_img: Optional["BytesIO"]=None) -> Player:
        # dummy object to runs the  validations
        validator = Player(0, username, discord_user_id, emoji, profile_img)
        validated_img_data = (validator.profile_img.getvalue()
                              if validator.profile_img is not None else None)

        result = self._create_dataset(dict(username=validator.username,
                                           discord_id=discord_user_id,
                                           emoji=validator.emoji,
                                           profile_img=validated_img_data),
                                      get_args=dict(discord_id=discord_user_id))

        return self._dataset_to_model(result)


    def get_by_discord_id(self, discord_id: int) -> Optional[Player]:
        dataset = self.dataset_cls().get_or_none(self.dataset_cls().discord_id == discord_id)
        return (dataset if dataset is None else self._dataset_to_model(dataset))
