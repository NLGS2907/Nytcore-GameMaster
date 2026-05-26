from typing import TYPE_CHECKING, Any

from peewee import BigIntegerField, BlobField, CharField

from gamemaster.db.base import BaseModel

if TYPE_CHECKING:
    from peewee import Database
    from peewee_migrate import Migrator


class PlayerDataset(BaseModel):
    username = CharField(max_length=30, null=False)
    discord_id = BigIntegerField(unique=True, null=False)
    emoji = CharField(null=True)
    profile_img = BlobField(null=True)


def migrate(migrator: "Migrator", database: "Database", fake: bool=False, **kwargs: Any):
    migrator.create_model(PlayerDataset)


def rollback(migrator: "Migrator", database: "Database", fake: bool=False, **kwargs: Any):
    migrator.remove_model(PlayerDataset)