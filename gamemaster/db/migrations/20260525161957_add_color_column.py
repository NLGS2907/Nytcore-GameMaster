from typing import TYPE_CHECKING, Any

from peewee import CharField

if TYPE_CHECKING:
    from peewee import Database
    from peewee_migrate import Migrator


def migrate(migrator: "Migrator", database: "Database", fake: bool=False, **kwargs: Any):
    migrator.add_fields("player", color=CharField(max_length=6, null=True))


def rollback(migrator: "Migrator", database: "Database", fake: bool=False, **kwargs: Any):
    migrator.remove_fields("player", "color")
