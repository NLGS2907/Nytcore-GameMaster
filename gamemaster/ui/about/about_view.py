from discord import ButtonStyle, SeparatorSpacing
from discord.ui import ActionRow, Button, Container, Section, Separator, TextDisplay, Thumbnail
from discord.utils import oauth_url

from ..base_view import BaseView

REPOSITORY_URL: str = r"https://github.com/NLGS2907/Nytcore-GameMaster"


class AboutView(BaseView):
    """View that displays info about the bot."""

    async def reset(self):
        invite_url = oauth_url(self.bot.application_id,
                               permissions=self.bot.preferred_permissions())
        section = Section(
            TextDisplay(f"## {self.bot.user.display_name}"),
            TextDisplay("_Little playground bot for\n"
                        "managing and playing games._"),
            accessory=Thumbnail(self.bot.user.display_avatar.url),
        )

        btn_row = ActionRow(
            Button(
                style=ButtonStyle.link,
                label="Invite",
                url=invite_url
            ),
            Button(
                style=ButtonStyle.link,
                label="Source",
                url=REPOSITORY_URL
            )
        )

        self.add_item(
            Container(
                section,
                # Separator(spacing=SeparatorSpacing.large),
                btn_row,
                Separator(spacing=SeparatorSpacing.large),
                TextDisplay(f"-# _Brought to you by NLGS (<@{self.bot.owner_id}>) dear._")
            )
        )
