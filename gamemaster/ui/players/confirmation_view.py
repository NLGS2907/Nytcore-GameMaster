from typing import TYPE_CHECKING, Optional, TypeAlias

from discord import SeparatorSpacing
from discord.ui import Container, Section, Separator, TextDisplay

from ..base_view import BaseView
from .countdown_loop import ConfirmationCountdownLoop
from .ready_btn import ReadyButton

if TYPE_CHECKING:
    from ...gamemaster import GameMaster
    from ...managers import GameManager
    from ...models import DiscordUserIdType
    from ..base_view import PossibleMessage, PossibleUser

_ReadyMap: TypeAlias = dict["DiscordUserIdType", bool]
_ReadyBtns: TypeAlias = dict["DiscordUserIdType", ReadyButton]
TIME_IN_SECS_PER_ITER: float = 1.0
ITERATIONS_UNTIL_READY: int = 5


class ConfirmationView(BaseView):
    """View for checking if all players are ready."""

    def __init__(self,
                 bot: "GameMaster",
                 parent_msg: "PossibleMessage",
                 origin_user: "PossibleUser",
                 *,
                 manager: "GameManager",
                 timeout: Optional[float]=None):
        """Initializes the lobby view.
        
        Apart from those of the parent class, this view includes some extra parameters.

        Args:
            manager: The manager of the underlying game.
        """

        super().__init__(bot, parent_msg, origin_user, timeout=timeout)
        self.manager: "GameManager" = manager
        self.__ready_map: _ReadyMap = {player.discord_user_id: False
                                       for player in self.manager.players}
        self._countdown_msg: Optional[str] = None
        self.__ready_btns: _ReadyBtns = {player_id: ReadyButton(self, player_id)
                                         for player_id in self.__ready_map}

        self.countdown: ConfirmationCountdownLoop = ConfirmationCountdownLoop(
            parent_view=self, count=ITERATIONS_UNTIL_READY
        )


    async def reset(self):
        container = Container(TextDisplay(f"# {self.manager.game_title()}"),
                              TextDisplay("Please press the buttons when ready."),
                              Separator(spacing=SeparatorSpacing.large, visible=True))

        if self._countdown_msg is not None:
            container.add_item(TextDisplay(self._countdown_msg))
            container.add_item(Separator(spacing=SeparatorSpacing.large, visible=True))

        for player in self.manager.players:
            emoji_str = ("" if player.emoji is None else f"{player.emoji} ")
            ready_btn = self.__ready_btns[player.discord_user_id]
            ready_btn.update()
            player_section = Section(TextDisplay(f"### {emoji_str}{player.username}"),
                                     accessory=ready_btn)

            container.add_item(player_section)
            container.add_item(Separator(spacing=SeparatorSpacing.small, visible=True))


        self.add_item(container)


    def _set_ready(self, user_id: "DiscordUserIdType", value: bool):
        """Sets a value in the internal ready map."""

        if user_id not in self.__ready_map:
            return
        self.__ready_map[user_id] = value


    def player_ready(self, user_id: "DiscordUserIdType"):
        """Marks a player as ready in the map.

        If a player with that ID doesn't exists, it does nothing.
        
        Args:
            user_id: The Discord user ID to search with.
        """

        self._set_ready(user_id, True)


    def player_not_ready(self, user_id: "DiscordUserIdType"):
        """Marks a player as NOT ready in the map.

        If a player with that ID doesn't exists, it does nothing.
        
        Args:
            user_id: The Discord user ID to search with.
        """

        self._set_ready(user_id, False)


    def all_players_ready(self) -> bool:
        """Checks if all the players are ready."""

        return all(self.__ready_map.values())


    def is_player_ready(self, user_id: "DiscordUserIdType") -> bool:
        """Checks if a player is ready by its Discord user ID.
        
        Args:
            user_id: The Discord user ID to search with.

        Returns:
            A boolean value indicating if the player is ready or not.
        """

        return self.__ready_map.get(user_id, False)


    def change_countdown_msg(self, current_loop: Optional[int]):
        """Generates the current countdown message given the current loop number."""

        msg = (f"All players ready. **Beggining game in {current_loop}...**"
               if current_loop is not None else None)
        self._countdown_msg = msg