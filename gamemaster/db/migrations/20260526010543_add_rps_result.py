from typing import TYPE_CHECKING, Any

from peewee import BigIntegerField, DateTimeField, ForeignKeyField

from gamemaster.db.base import BaseModel
from gamemaster.db.datasets import PlayerDataset

if TYPE_CHECKING:
    from peewee import Database
    from peewee_migrate import Migrator


class RPSResultDataset(BaseModel):
    player_1 = ForeignKeyField(PlayerDataset, backref="rps_games_as_first")
    player_2 = ForeignKeyField(PlayerDataset, backref="rps_games_as_second")
    rounds = BigIntegerField()
    saved = DateTimeField()


def migrate(migrator: "Migrator", database: "Database", fake: bool=False, **kwargs: Any):
    migrator.create_model(RPSResultDataset)


def rollback(migrator: "Migrator", database: "Database", fake: bool=False, **kwargs: Any):
    migrator.remove_model(RPSResultDataset)