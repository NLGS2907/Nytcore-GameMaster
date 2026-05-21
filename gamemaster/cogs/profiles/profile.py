from typing import TYPE_CHECKING, Optional

# discord.py actually uses these classes, even if here it's only for type hints
from discord import Member
from discord.app_commands import command, describe

from ...embeds import ProfileEmbed
from ...modals import ProfileEditModal
from ..cog_base import _BaseCog, _BaseGroup
from ...ui import ProfileView

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
              compact=("Wether to show the profile in compact form with an embed, "
                       "or use the new V2 components."),
              public="Wether the message generated can be seen by others or only you.")
    async def show_profile(self,
                           interaction: "Interaction",
                           player: Optional[Member]=None,
                           compact: bool=False,
                           public: bool=False):
        await interaction.response.defer(ephemeral=not public)

        player_user = player or interaction.user
        game_player = self.bot.repositories.player.create(player_user.name, player_user.id)

        if compact:
            profile_embed = ProfileEmbed(self.bot, game_player, player_user)
            await profile_embed.prepare()
            msg = await interaction.followup.send(wait=True, # So it returns the message
                                                  # needed for embed to use local image URL
                                                  file=profile_embed.thumbnail_file,
                                                  embed=profile_embed,
                                                  ephemeral=not public)
        else:
            profile_view = ProfileView(self.bot, await interaction.original_response(),
                                       game_player, player_user)
            await profile_view.prepare()
            msg = await interaction.followup.send(wait=True, # So it returns the message
                                                  # needed for view to use local image URL
                                                  files=profile_view.all_files,
                                                  view=profile_view,
                                                  ephemeral=not public)

        if public:
            await msg.delete(delay=15.0)


    @command(name="edit",
             description="Edit profile details.")
    async def edit_profile(self, interaction: "Interaction"):
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
