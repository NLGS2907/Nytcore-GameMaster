from typing import TYPE_CHECKING, Optional

from discord.app_commands import Choice, choices, command, describe

from ...ui.games import GameManager, GameSelectorView
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
                   for game_id, title in GameManager.walk_ids_titles()])
    async def choose_game(self, interaction: "Interaction", game: Optional[Choice[int]]=None):
        await interaction.response.defer(ephemeral=True)

        if game is not None:
            # TODO: replace this with the lobby
            chosen_game = GameManager.class_with_id(game.value)
            msg_content = (f"_Proceeding with game {chosen_game.game_title!r}_"
                           if chosen_game is not None else "_Somehow, no game was selected._")
            await interaction.followup.send(msg_content, ephemeral=True)
            return

        selector_view = GameSelectorView(self.bot,
                                         await interaction.original_response(),
                                         interaction.user)
        await interaction.followup.send(view=selector_view, ephemeral=True)


async def setup(bot: "GameMaster"):
    """Adds this cog to the bot."""

    await bot.add_cog(GamesCog(bot))
