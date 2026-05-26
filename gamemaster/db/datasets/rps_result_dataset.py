from peewee import BigIntegerField, DateTimeField, ForeignKeyField

from ..base import BaseModel
from ..datasets import PlayerDataset


class RPSResultDataset(BaseModel):
    player_1 = ForeignKeyField(PlayerDataset, backref="rps_games_as_first")
    player_2 = ForeignKeyField(PlayerDataset, backref="rps_games_as_second")
    rounds = BigIntegerField()
    saved = DateTimeField()