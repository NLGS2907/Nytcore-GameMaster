from os import execl
from sys import executable
from typing import TYPE_CHECKING

from discord.app_commands import command
from discord.app_commands.errors import CheckFailure

from ..cog_base import _BaseCog, _BaseGroup

if TYPE_CHECKING:
    from discord import Interaction
    from discord.app_commands.errors import AppCommandError

    from ...gamemaster import GameMaster
    from ..cog_base import GroupsList


class DevGroup(_BaseGroup):
    """Group for commands meant for developers."""

    def __init__(self, bot: "GameMaster") -> None:
        """Initializes the dev command group.

        Args:
            bot: The bot instance to link to this group.
        """

        super().__init__(bot,
                         name="dev",
                         description="Commands for developers.")

    async def interaction_check(self, interaction: "Interaction") -> bool:
        """Verifies if the user ivoking the command is authorized to do so."""

        return await self.bot.is_owner(interaction.user)


    async def on_error(self, interaccion: "Interaction", error: "AppCommandError") -> None:
        """Alerts the user that the command invocation failed."""

        if isinstance(error, CheckFailure):
            mensaje = (f"How strange! It seems that you, {interaccion.user.mention}, don't "
                       "have enough clearance for this command.")
            await interaccion.response.send_message(content=mensaje,
                                                    ephemeral=True)
            return

        raise error from error


    @command(name="reboot",
             description="[OWNER] Reboots the bot.")
    async def reboot(self, interaction: "Interaction") -> None:
        """Disconnects, shuts down, and then reconnects the bot again."""

        if not executable:
            mensaje = "Could not reboot the bot."

            await interaction.response.send_message(content=f"**[ERROR]** {mensaje}",
                                                    ephemeral=True)
            self.bot.log.error(mensaje)
            return

        await interaction.response.send_message(content="Rebooting...",
                                                ephemeral=True)
        self.bot.log.info(f"Rebooting {self.bot.user}...")

        # we also close it, just in case
        await self.bot.shutdown()

        execl(executable, executable, "-m", "gamemaster")


    @command(name="shutdown",
             description="[OWNER] Shuts down the bot.")
    async def shutdown(self, interaction: "Interaction") -> None:
        """Shuts down the bot and disconnects it"""

        await interaction.response.send_message(content=f"Shutting {self.bot.user.name} down...",
                                                ephemeral=True)
        await self.bot.shutdown()


class AdminCog(_BaseCog):
    """Cog for administrator commands."""

    @classmethod
    def groups(cls) -> "GroupsList":
        return [DevGroup]


async def setup(bot: "GameMaster"):
    """Adds this cog to the bot."""

    await bot.add_cog(AdminCog(bot))
