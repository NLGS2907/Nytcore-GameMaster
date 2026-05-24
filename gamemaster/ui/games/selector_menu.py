from typing import TYPE_CHECKING, Optional

from discord import PartialEmoji, SelectOption
from discord.ui import Select

from ...managers import GameManager
from ..lobby import LobbyView
from ..throwable_view import ThrowableView

if TYPE_CHECKING:
    from discord import Interaction, InteractionMessage

    from ...gamemaster import GameMaster
    from ..base_view import PossibleUser


class GameSelectionMenu(Select):
    """Menu that chooses the relevant games from the list."""

    def __init__(self,
                 bot: "GameMaster",
                 parent_msg: "InteractionMessage",
                 origin_user: "PossibleUser"):
        """Initializes the selector menu.
        
        Args:
            bot: A reference to the bot user.
            parent_msg: A reference to the parent message that spawned this view.
            origin_user: The orignal user who sent the interaction. The parent message not
                         necessarily holds this information, as the bot is the author most of
                         the time.
        """

        super().__init__(placeholder="Choose a game!",
                         min_values=1,
                         max_values=1,
                         options=self._generate_options(),
                         disabled=False,
                         required=True)

        self.bot: "GameMaster" = bot
        self.origin_msg: "InteractionMessage" = parent_msg
        self.origin_user: "PossibleUser" = origin_user


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
            for game_manager_cls in sorted(GameManager.all_games(), key=lambda man: man.game_id())
        ]


    def _retrieve_value(self) -> Optional[GameManager]:
        """Retrieves the manager selected in the menu, if available."""

        if not self.values:
            return None

        return GameManager.class_with_id(int(self.values[0]))(self.bot)


    async def callback(self, interaction: "Interaction"):
        chosen_game = self._retrieve_value()
        lobby_view = LobbyView(self.bot, self.origin_msg, self.origin_user,
                               manager=chosen_game, timeout=None)

        await lobby_view.reset()
        await interaction.response.edit_message(view=ThrowableView("_Lobby created!_"))
        message = await interaction.channel.send(view=lobby_view)
        lobby_view.parent_msg = message
