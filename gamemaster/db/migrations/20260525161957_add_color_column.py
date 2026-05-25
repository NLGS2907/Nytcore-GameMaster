from typing import TYPE_CHECKING, Any

from peewee import CharField

from gamemaster.db.datasets import PlayerDataset

if TYPE_CHECKING:
    from peewee import Database
    from peewee_migrate import Migrator

COLOR_MAX_LENGTH: int = 6


def migrate(migrator: "Migrator", database: "Database", fake: bool=False, **kwargs: Any):
    migrator.add_fields(PlayerDataset, color=CharField(max_length=COLOR_MAX_LENGTH, null=True))


def rollback(migrator: "Migrator", database: "Database", fake: bool=False, **kwargs: Any):
    migrator.remove_fields(PlayerDataset, "color")
