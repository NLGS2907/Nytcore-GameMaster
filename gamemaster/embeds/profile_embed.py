from typing import TYPE_CHECKING, Optional

from discord import Colour, Embed, File

from ..models import IMG_FORMAT

if TYPE_CHECKING:
    from discord.abc import User

    from ..gamemaster import GameMaster
    from ..models import Player


class ProfileEmbed(Embed):
    """Exclusive embed for detailing player information."""

    def __init__(self, bot: "GameMaster", player: "Player", user: "User"):
        """Initializes the profile embed.
        
        Args:
            player: The player from where to acquire info.
            user: The discord user linked to the player.
        """

        super().__init__(title=f"\"{player.username}\" Profile",
                         colour=(Colour.from_str(player.fav_color)
                                 if player.fav_color is not None
                                 else Colour.random()))

        self.bot: "GameMaster" = bot
        self.player: "Player" = player
        self.discord_user: "User" = user
        self.thumbnail_file: Optional[File] = None


    async def prepare(self):
        """Preconfigures this embed to send it later."""
        
        author_img = await self.bot.fetch_avatar(self.discord_user)

        user_img = self.player.profile_img
        img_props = self.player.image_properties

        thumbnail = (user_img if user_img is not None else author_img)
        emoji_val = (self.player.emoji if self.player.emoji is not None else "*None*")
        img_val = (f"*{img_props["format"].upper()} of dimensions "
                   f"{img_props['width']}x{img_props['height']} px*"
                   if user_img is not None else "*None*")

        self.thumbnail_file = File(thumbnail, filename=f"thumbnail.{IMG_FORMAT}")
        self.set_thumbnail(url=f"attachment://{self.thumbnail_file.filename}")\
            .set_author(name=self.discord_user.display_name,
                        icon_url=self.discord_user.display_avatar.url)\
            .add_field(name="Name", value=self.player.username, inline=True)\
            .add_field(name="Discord User", value=self.discord_user.mention, inline=True)\
            .add_field(name="Emoji", value=emoji_val, inline=True)\
            .add_field(name="Image Details", value=img_val, inline=True)
