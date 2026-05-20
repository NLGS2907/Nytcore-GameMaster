from typing import TYPE_CHECKING, Optional

# discord.py actually uses these classes, even if here it's only for type hints
from discord import Member
from discord.app_commands import command, describe

from ...embeds import ProfileEmbed
from ...modals import ProfileEditModal
from ..cog_base import _BaseCog, _BaseGroup

if TYPE_CHECKING:
    from discord import Interaction, Member

    from ...gamemaster import GameMaster
    from ..cog_base import GroupsList


class ProfileGroup(_BaseGroup):
    """Group for commands related to player profiles."""

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
    @describe(player="The player whose profile to fetch.",
              ephemeral="Wether the message generated can only be seen by you or by others.")
    async def show_profile(self,
                           interaction: "Interaction",
                           player: Optional[Member]=None,
                           ephemeral: bool=True):
        """Show the profile info of a player to the user."""

        await interaction.response.defer(ephemeral=ephemeral)

        player_user = player or interaction.user
        game_player = self.bot.repositories.player.create(player_user.name, player_user.id)

        profile_embed = ProfileEmbed(game_player, player_user)
        await profile_embed.prepare()

        msg = await interaction.followup.send(wait=True, # So it returns the message
                                              # needed for embed to use local image URL
                                              file=profile_embed.thumbnail_file,
                                              embed=profile_embed,
                                              ephemeral=ephemeral)

        if not ephemeral:
            await msg.delete(delay=15.0)


    @command(name="edit",
             description="Edit profile details.")
    async def edit_profile(self, interaction: "Interaction"):
        """Edits the player profile with a pop-up."""

        game_player = self.bot.repositories.player.create(interaction.user.name,
                                                          interaction.user.id)

        await interaction.response.send_modal(ProfileEditModal(game_player,
                                                               self.bot.repositories.player))


class ProfileCog(_BaseCog):
    """Cog for commands related to player profiles."""

    @classmethod
    def groups(cls) -> "GroupsList":
        return [ProfileGroup]


async def setup(bot: "GameMaster"):
    """Adds this cog to the bot."""

    await bot.add_cog(ProfileCog(bot))
