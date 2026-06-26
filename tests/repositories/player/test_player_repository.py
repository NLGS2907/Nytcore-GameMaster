from unittest import TestCase
from unittest.mock import Mock, patch

from gamemaster.db.datasets import PlayerDataset
from gamemaster.models import Player
from gamemaster.repositories import PlayerRepository


class TestPlayerRepository(TestCase):
    def setUp(self):
        self.ds_id = 123456789
        self.player_mock = Mock(Player, **{
            "id": 1,
            "username": "Billy",
            "discord_user_id": self.ds_id,
            "emoji": None
        })
        record_dataset_mock = Mock(PlayerDataset, **{
            "profile_img": b""
        })
        self.player_dataset_mock = Mock(PlayerDataset)
        self.player_dataset_mock.get_or_none.return_value = record_dataset_mock

        self.player_repo = PlayerRepository()
        self.player_repo.dataset_cls = self.player_dataset_mock


    def test_transforms_emoji_into_unicode(self):
        emoji = "⚡"

        self.assertEqual(self.player_repo.emoji_to_unicode(emoji), "U+26A1")


    def test_transforms_unicode_into_emoji(self):
        unicode = "U+1F525"

        self.assertEqual(self.player_repo.unicode_to_emoji(unicode), "🔥")



    def test_recovers_a_player_by_discord_id(self):
        with patch.object(self.player_repo, '_dataset_to_model', return_value=self.player_mock):
            result = self.player_repo.get_by_discord_id(self.ds_id)
            
            self.assertEqual(result, self.player_mock)

