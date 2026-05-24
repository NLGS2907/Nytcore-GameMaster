from typing import TYPE_CHECKING, Optional

from discord.app_commands import Choice, choices, command, describe

from ...managers import GameManager
from ...ui import LobbyView
from ...ui.games import GameSelectorView
from ..cog_base import _BaseCog

if TYPE_CHECKING:
    from discord import Interaction

    from ...gamemaster import GameMaster


class GamesCog(_BaseCog):
    """General cog for interacting with games."""

    @command(name="play",
             description="Pretty self-explanatory. Choose a game!")
    @describe(game="The game to play, if not chosen here then a selection menu will appear.")
    @choices(game=[Choice(name=title, value=game_id)
                   for game_id, title in sorted(GameManager.walk_ids_titles(),
                                                key=lambda t: t[0])])
    async def choose_game(self, interaction: "Interaction", game: Optional[Choice[int]]=None):
        await interaction.response.defer(ephemeral=True)
        original_msg = await interaction.original_response()

        if game is not None:
            chosen_game_cls = GameManager.class_with_id(game.value)
            lobby_view = LobbyView(self.bot, original_msg, interaction.user,
                                   manager=chosen_game_cls(self.bot), timeout=None)
            await lobby_view.reset()
            await interaction.followup.send("_Lobby created!_", ephemeral=True)
            message = await interaction.channel.send(view=lobby_view)
            lobby_view.parent_msg = message
            return

        selector_view = GameSelectorView(self.bot,
                                         original_msg,
                                         interaction.user)
        await interaction.followup.send(view=selector_view, ephemeral=True)


async def setup(bot: "GameMaster"):
    """Adds this cog to the bot."""

    await bot.add_cog(GamesCog(bot))
