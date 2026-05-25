from typing import TYPE_CHECKING

from discord.app_commands.errors import CheckFailure

if TYPE_CHECKING:
    from discord import Interaction
    from discord.app_commands.errors import AppCommandError


class _AdminCheckMixin:
    """Mixin class for implementing admin interaction checks on cogs and groups.
    
    Do note that, if inherited along a Cog or a Group, this class SHOULD BE FIRST in the MRO.
    Otherwise, it will be overwritten with the empty implementation that those classes bring.
    """

    async def interaction_check(self, interaction: "Interaction") -> bool:
        """Verifies if the user invoking the command is authorized to do so."""

        if not getattr(self, "bot"):
            return False

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
