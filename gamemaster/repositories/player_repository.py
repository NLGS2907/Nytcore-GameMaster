from io import BytesIO
from typing import Optional

from ..db.datasets import PlayerDataset
from ..models import Player
from .base_repository import BaseRepository


class PlayerRepository(BaseRepository):
    @staticmethod
    def dataset_cls():
        return PlayerDataset

    def _model_to_dataset(self, model: Player) -> PlayerDataset:
        return PlayerDataset(username=model.username,
                             discord_id=model.discord_user.id,
                             emoji=f"U+{ord(model.emoji):X}",
                             profile_img=model.profile_img)


    def _dataset_to_model(self, dataset: PlayerDataset) -> Player:
        if dataset.profile_img is None:
            img_file = None
        else:
            img_file = BytesIO(dataset.profile_img)
            img_file.seek(0)

        return Player(dataset.username,
                      dataset.discord_id,
                      (dataset.emoji if dataset.emoji is None else chr(int(dataset.emoji[2:]), 16)),
                      img_file)


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

        dataset = self.dataset_cls()
        result = self._create_dataset(dict(username=username,
                                           discord_id=discord_user_id,
                                           emoji=emoji,
                                           profile_img=profile_img),
                                      preserve_args=[dataset.username,
                                                     dataset.emoji,
                                                     dataset.profile_img])

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
