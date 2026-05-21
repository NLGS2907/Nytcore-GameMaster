"""Module for listening to events."""

from typing import TYPE_CHECKING

from discord.ext.commands import Cog

from ..cog_base import _BaseCog

if TYPE_CHECKING:
    from discord import Guild

    from ...gamemaster import GameMaster


class EventsCog(_BaseCog):
    """Events listener."""

    @Cog.listener()
    async def on_ready(self):
        """The bot has finished the setup and is ready to use."""

        self.bot.log.info(f"{self.bot.user} is ready!")


    @Cog.listener()
    async def on_disconnect(self):
        """The bot has lost connection."""

        self.bot.log.info(f"{self.bot.user.display_name} has lost connection.")


    @Cog.listener()
    async def on_resumed(self) -> None:
        """The bot has resumed a session, having lost it prior."""

        self.bot.log.info("Recovered connection. Resuming session...")


    @Cog.listener()
    async def on_guild_join(self, guild: "Guild") -> None:
        """The bot has joined a guild for the first time."""

        self.bot.log.info(f"The bot has joined guild {guild.name!r}")


async def setup(bot: "GameMaster"):
    """Adds this cog to the bot."""

    await bot.add_cog(EventsCog(bot))
