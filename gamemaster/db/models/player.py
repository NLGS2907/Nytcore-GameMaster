"""Player model module."""

from peewee import BlobField, CharField, BigIntegerField

from .. import BaseModel

USERNAME_MAX_LENGTH: str = 30

class PlayerDataset(BaseModel):
    """Player model that connects with the database."""

    username = CharField(max_length=USERNAME_MAX_LENGTH)
    discord_id = BigIntegerField(unique=True)
    emoji = CharField()
    profile_img = BlobField()
