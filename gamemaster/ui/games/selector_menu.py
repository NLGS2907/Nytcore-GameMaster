from typing import TYPE_CHECKING, Optional

from discord import PartialEmoji, SelectOption
from discord.ui import Select

from ...managers import GameManager

if TYPE_CHECKING:
    from discord import Interaction


class GameSelectionMenu(Select):
    """Menu that chooses the relevant games from the list."""

    def __init__(self):
        """Initializes the selector menu."""

        super().__init__(placeholder="Choose a game!",
                         min_values=1,
                         max_values=1,
                         options=self._generate_options(),
                         disabled=False,
                         required=True)


    def _generate_options(self) -> list[SelectOption]:
        """Generate all the game options and their handlers."""

        return [
            SelectOption(
                label=game_manager_cls.game_title(),
                value=game_manager_cls.game_id(),
                description=game_manager_cls.game_description(),
                emoji=PartialEmoji.from_str(game_manager_cls.random_emoji()),
                default=False
            )
            for game_manager_cls in GameManager.all_games()
        ]


    def _retrieve_value(self) -> Optional[GameManager]:
        """Retrieves the manager selected in the menu, if available."""

        if not self.values:
            return None

        return GameManager.class_with_id(int(self.values[0]))


    async def callback(self, interaction: "Interaction"):
        # TODO: replace this with the lobby
        chosen_game = self._retrieve_value()
        msg_content = (f"_Proceeding with game {chosen_game.game_title()!r}_"
               if chosen_game is not None else "_Somehow, no game was selected._")
        await interaction.response.send_message(msg_content, ephemeral=True)
