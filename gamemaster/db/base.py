"""Module for generating base models for the database."""

__all__ = ["db"]

from os import getenv
from typing import Self

from peewee import Model, SqliteDatabase

MODEL_SUFFIX: str = "dataset"

db = SqliteDatabase(getenv("DATABASE_PATH"))

class BaseModel(Model):
    """Base class for creating all object models."""

    children = []

    class Meta:
        database = db

        def name_without_suffix(model_cls: Self) -> str:
            return model_cls.__name__.lower().removesuffix(MODEL_SUFFIX)
        table_function = name_without_suffix


    def __init_subclass__(cls):
        __class__.children.append(cls)
