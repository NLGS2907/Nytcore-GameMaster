from collections import deque
from io import StringIO
from typing import TYPE_CHECKING

from discord import File
from discord.app_commands import command, describe

from ...logger import GAMEMASTER_NAMESPACE, get_log_path
from ..cog_base import _BaseCog, _BaseGroup
from ._admin_check import _AdminCheckMixin

if TYPE_CHECKING:
    from discord import Interaction

    from ...gamemaster import GameMaster
    from ..cog_base import GroupsList

DISCORD_MAX_CHARS: int = 2000


class LogGroup(_AdminCheckMixin, _BaseGroup):
    """Group for commands meant for developers."""

    def __init__(self, bot: "GameMaster") -> None:
        """Initializes the dev command group.

        Args:
            bot: The bot instance to link to this group.
        """

        super().__init__(bot,
                         name="log",
                         description="Commands for using the application logger.")


    @staticmethod
    def _less_than_n_chars(string: str, max_chars: int) -> bool:
        """Detects if a string has `max_chars` characters or more.

        This implementation stops early, so it is preferable to `len()`.

        Args:
            string: The text to evaluate.
            max_chars: The amount of characters to use as threshold.

        Returns:
            A boolean value with a value of `False` in case the amount of chars exceed the given
            threshold, or `True` if it doesn't.
        """

        count = 0
        for _ in string:
            count += 1
            if count >= max_chars:
                return False

        return True


    @command(name="get",
             description="[OWNER] Retrieves the entire log file.")
    async def log_get(self, interaction: "Interaction"):
        log_path = get_log_path(GAMEMASTER_NAMESPACE)
        await interaction.response.send_message(
            file=File(log_path, filename=log_path.lstrip("./")),
            ephemeral=True
        )


    @command(name="tail",
             description="[OWNER] Shows the last lines of the log file.")
    @describe(n="The amount of lines to show.")
    async def log_tail(self, interaction: "Interaction", n: int=15):
        lines = []
        with open(get_log_path(GAMEMASTER_NAMESPACE), mode="r", encoding="utf-8") as arch:
            lines.extend(deque(arch, n))
        message = "".join(lines)

        if self._less_than_n_chars(message, DISCORD_MAX_CHARS - 10):
            await interaction.response.send_message(f"```\n{message}```",
                                                    ephemeral=True)
            return

        archivo_log = StringIO(message)
        await interaction.response.send_message(
            file=File(archivo_log,
                      filename=f"gamemaster_last_{n}_lines.log"),
            ephemeral=True)


    @command(name="purge",
             description="[OWNER] Flushes the enitre contents of the log file, rendering it blank.")
    async def log_purge(self, interaction: "Interaction"):
        log_path = get_log_path(GAMEMASTER_NAMESPACE)
        lines = 0

        with open(log_path, mode="rb") as file:
            lines += sum(1 for line in file if line.strip())

        with open(log_path, mode="w"):
            pass # we open it only to overwrite the contents

        await interaction.response.send_message(f"Emptied log file `{log_path}`.\n"
                                                f"Deleted `{lines}` lines.",
                                                ephemeral=True)


class LogCog(_BaseCog):
    """Cog for administrator commands."""

    @classmethod
    def groups(cls) -> "GroupsList":
        return [LogGroup]


async def setup(bot: "GameMaster"):
    """Adds this cog to the bot."""

    await bot.add_cog(LogCog(bot))
