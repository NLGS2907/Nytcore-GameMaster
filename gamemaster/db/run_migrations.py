"""Module for executing database migrations."""

from os import getenv
from pathlib import Path
from re import compile

from peewee_migrate import Router

from .base import db


def run_migrations():
    """Makes all the migrations, in order, of the database."""

    db_dir = Path(getenv("DATABASE_PATH")).parent
    router = Router(db, migrate_dir=(db_dir / "migrations"), migrate_table="_migration_history")
    router.filemask = compile(r"[\d]{14}_[^\.]+\.py$") # so that timestamps are allowed

    router.run()
