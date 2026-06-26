from unittest import TestCase

from peewee import BlobField, DateTimeField, ForeignKeyField

from gamemaster.db.datasets import RPSResultDataset


class TestRPSResultDataset(TestCase):
    def test_has_all_fields(self):
        self.assertIsInstance(RPSResultDataset.player_1, ForeignKeyField)
        self.assertIsInstance(RPSResultDataset.player_2, ForeignKeyField)
        self.assertIsInstance(RPSResultDataset.rounds, BlobField)
        self.assertIsInstance(RPSResultDataset.saved, DateTimeField)
