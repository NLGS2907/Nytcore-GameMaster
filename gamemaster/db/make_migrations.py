"""Module for executing database migrations."""

from importlib import import_module
from os import getenv
from pathlib import Path

from playhouse.migrate import SqliteMigrator

from ..files import search_files
from .base import BaseModel, db


def make_migrations():
    """Makes all the migrations, in order, of the database.
    
    As a bonus, it also prevently creates all relevant tables.
    """

    db_dir = Path(getenv("DATABASE_PATH")).parent
    ext = ".py"

    with db:
        db.create_tables(BaseModel.children)
        migrator = SqliteMigrator(db)

        modules = sorted((import_module(module.removesuffix(f"{ext}").replace("/", "."), ".") 
                          for module in 
                          search_files(f"*{ext}",
                                      (db_dir / "migrations").as_posix(),
                                      recursive=False,
                                      ignore_patterns=("__init__.*",))),
                        key=lambda mod: mod.__name__)

        for module in modules:
            with db.atomic():
                if hasattr(module, "migration"):
                    module.migration(migrator)


