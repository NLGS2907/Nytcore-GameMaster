from typing import TYPE_CHECKING

from discord.app_commands import command

from ...repositories import PlayerRepository
from ..cog_base import _BaseCog, _BaseGroup

if TYPE_CHECKING:
    from discord import Interaction

    from ...gamemaster import GameMaster
    from ..cog_base import GroupsList


class ProfileGroup(_BaseGroup):
    """Group for commands related to profile commands"""

    def __init__(self, bot: "GameMaster") -> None:
        """Initializes the profile command group.

        Args:
            bot: The bot instance to link to this group.
        """

        super().__init__(bot,
                         name="profile",
                         description="Commands to tinker with the player profile.")


    @command(name="show",
             description="Shows all profile info.")
    async def show_profile(self, interaction: "Interaction"):
        player_repo = PlayerRepository()
        player = player_repo.create(interaction.user.name, interaction.user.id)

        await interaction.response.send_message(f"PONG:\n{player.username = }\n{player.discord_user_id = }")


class ProfileCog(_BaseCog):
    """Cog for commands related to player profiles."""

    @classmethod
    def groups(cls) -> "GroupsList":
        return [ProfileGroup]


async def setup(bot: "GameMaster"):
    """Adds this cog to the bot."""

    await bot.add_cog(ProfileCog(bot))
