"""Module for generating base models for the database."""

from os import getenv
from peewee import SqliteDatabase, Model

db = SqliteDatabase(getenv("DATABASE_PATH"))

class BaseModel(Model):
    """Base class for creating all object models."""

    children = []

    class Meta:
        database = db


    def __init_subclass__(cls):
        __class__.children.append(cls)
