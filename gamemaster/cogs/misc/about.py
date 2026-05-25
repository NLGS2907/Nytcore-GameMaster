from typing import TYPE_CHECKING

from discord.app_commands import command

from ...ui import AboutView
from ..cog_base import _BaseCog

if TYPE_CHECKING:
    from discord import Interaction

    from ...gamemaster import GameMaster


class AboutCog(_BaseCog):
    """Cog for commands that retrieve information about the bot."""

    @command(name="about",
             description="Displays basic information about the GameMaster.")
    async def show_about(self, interaction: "Interaction"):
        await interaction.response.defer(ephemeral=True)

        about_view = AboutView(self.bot,
                               await interaction.original_response(),
                               interaction.user,
                               timeout=5.0)
        await about_view.reset()
        await interaction.followup.send(view=about_view, ephemeral=True)







async def setup(bot: "GameMaster"):
    """Adds this cog to the bot."""

    await bot.add_cog(AboutCog(bot))
