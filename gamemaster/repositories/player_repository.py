from io import BytesIO

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
