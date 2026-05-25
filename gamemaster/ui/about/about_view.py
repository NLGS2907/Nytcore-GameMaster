from discord import SeparatorSpacing
from discord.ui import Container, Section, Separator, TextDisplay, Thumbnail
from discord.utils import oauth_url

from ..base_view import BaseView


class AboutView(BaseView):
    """View that displays info about the bot."""

    async def reset(self):
        invite_url = oauth_url(self.bot.application_id,
                               permissions=self.bot.preferred_permissions())
        section = Section(
            TextDisplay(f"## {self.bot.user.display_name}"),
            TextDisplay(f"* [**Invite**]({invite_url})"),
            TextDisplay("* [**Source**](https://github.com/NLGS2907/Nytcore-GameMaster)"),
            accessory=Thumbnail(self.bot.user.display_avatar.url),
        )

        self.add_item(
            Container(
                section,
                Separator(spacing=SeparatorSpacing.large),
                TextDisplay(f"-# _Brought to you by NLGS (<@{self.bot.owner_id}>) dear._")
            )
        )
