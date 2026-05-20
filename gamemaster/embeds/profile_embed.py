from io import BytesIO
from typing import TYPE_CHECKING, Optional

from discord import Colour, Embed, File
from PIL.Image import open as img_open

from ..models import IMG_FORMAT

if TYPE_CHECKING:
    from discord.abc import User

    from ..models import Player


class ProfileEmbed(Embed):
    """Exclusive embed for detailing player information."""

    def __init__(self, player: "Player", user: "User"):
        """Initializes the profile embed.
        
        Args:
            player: The player from where to acquire info.
            user: The discord user linked to the player.
        """

        super().__init__(title=f"{player.username} information",
                         colour=Colour.random())

        self.player: "Player" = player
        self.discord_user: "User" = user
        self.thumbnail_file: Optional[File] = None


    async def prepare(self):
        """Preconfigures this embed to send it later."""

        author_img = BytesIO()
        await self.discord_user.display_avatar.with_format(IMG_FORMAT).save(author_img,
                                                                            seek_begin=True)

        user_img = self.player.profile_img

        if user_img is not None:
            with img_open(user_img) as im:
                fmt = im.format
                img_w, img_h = im.size
            user_img.seek(0)

        thumbnail = (user_img if user_img is not None else author_img)
        emoji_val = (self.player.emoji if self.player.emoji is not None else "*Ninguno*")
        img_val = (f"*{fmt.upper()} of size {img_w}x{img_h} px*"
                   if user_img is not None
                   else "*None*")

        self.thumbnail_file = File(thumbnail, filename=f"thumbnail.{IMG_FORMAT}")
        self.set_thumbnail(url=f"attachment://thumbnail.{IMG_FORMAT}")\
            .set_author(name=self.discord_user.display_name,
                        icon_url=self.discord_user.display_avatar.url)\
            .add_field(name="Name", value=self.player.username, inline=True)\
            .add_field(name="id", value=self.player.discord_user_id, inline=True)\
            .add_field(name="Emoji", value=emoji_val, inline=True)\
            .add_field(name="Image", value=img_val, inline=True)
