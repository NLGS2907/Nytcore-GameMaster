from peewee import DateTimeField, ForeignKeyField, IntegerField

from ..base import BaseModel
from ..datasets import PlayerDataset


class RPSResultDataset(BaseModel):
    player_1 = ForeignKeyField(PlayerDataset, backref="rps_games_as_first")
    player_2 = ForeignKeyField(PlayerDataset, backref="rps_games_as_second")
    rounds = IntegerField()
    saved = DateTimeField()