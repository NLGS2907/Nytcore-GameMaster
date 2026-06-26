from unittest import TestCase

from peewee import BigIntegerField, BlobField, CharField

from gamemaster.db.datasets import PlayerDataset


class TestPlayerDataset(TestCase):
    def test_has_all_fields(self):
        self.assertIsInstance(PlayerDataset.username, CharField)
        self.assertIsInstance(PlayerDataset.discord_id, BigIntegerField)
        self.assertIsInstance(PlayerDataset.emoji, CharField)
        self.assertIsInstance(PlayerDataset.profile_img, BlobField)
        self.assertIsInstance(PlayerDataset.color, CharField)
