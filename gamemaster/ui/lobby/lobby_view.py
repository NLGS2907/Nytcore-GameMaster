from typing import TYPE_CHECKING, Optional, TypeAlias

from discord import SeparatorSpacing
from discord.ui import ActionRow, Container, Separator, TextDisplay

from ..base_view import BaseView
from .begin_game_btn import BeginGameButton
from .close_lobby_btn import CloseLobbyButton
from .join_btn import JoinButton
from .leave_btn import LeaveButton
from .settings_btn import SettingsButton

if TYPE_CHECKING:
    from ...gamemaster import GameMaster
    from ...managers import GameManager
    from ...models import Player
    from ..base_view import PossibleMessage, PossibleUser

PlayersList: TypeAlias = list["Player"]


class LobbyView(BaseView):
    """View for a waiting gaming lobby."""

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
        self.manager.add_player(self.player_from_user(self.user))

        self.__players_len: int = len(self.manager.players)

        self.__close_lobby_btn: CloseLobbyButton = CloseLobbyButton(self)
        self.__begin_game_btn: BeginGameButton = BeginGameButton(self)
        self.__leave_btn: LeaveButton = LeaveButton(self)
        self.__join_btn: JoinButton = JoinButton(self)
        self.__settings_btn: SettingsButton = SettingsButton(self)


    async def reset(self):
        container = Container(TextDisplay(f"# {self.manager.game_title()}"))

        game_desc = self.manager.game_description()
        if game_desc is not None:
            container.add_item(TextDisplay(game_desc))

        container.add_item(Separator(spacing=SeparatorSpacing.large, visible=True))
        lobby_row = ActionRow(self.__close_lobby_btn)
        if self.enough_players():
            lobby_row.add_item(self.__begin_game_btn)
        container.add_item(lobby_row)

        container.add_item(Separator(spacing=SeparatorSpacing.small, visible=True))
        container.add_item(TextDisplay(f"## Players in Lobby ({self.players_len}/"
                                       f"{self.manager.max_players()})"))

        for player in self.manager.players:
            discord_mention = f"<@{player.discord_user_id}>"
            emoji_str = ("" if player.emoji is None else f"{player.emoji}  ")
            host_str = ("\t-\t**HOST**" if player.discord_user_id == self.user.id else "")
            container.add_item(TextDisplay(f"* {emoji_str}{player.username}\t({discord_mention})"
                                           f"{host_str}"))

        is_full = self.players_full()
        players_row = ActionRow(self.__leave_btn)
        if not is_full:
            players_row.add_item(self.__join_btn)
        container.add_item(players_row)

        container.add_item(Separator(spacing=SeparatorSpacing.small))
        container.add_item(ActionRow(self.__settings_btn))

        self.add_item(container)


    @property
    def players_len(self) -> int:
        """Lazy loads and returns the amount of players."""

        return self.__players_len


    def not_enough_players(self) -> bool:
        """Checks if the amount of players is below the minimum allowed."""

        return self.players_len < self.manager.min_players()


    def players_full(self) -> bool:
        """Checks if the amount of players exceeds or is equal to the maximum allowed."""

        return self.players_len >= self.manager.min_players()


    def enough_players(self) -> bool:
        """Checks if the amount of players is just right to start the game."""

        return self.manager.min_players() <= self.players_len <= self.manager.max_players()


    def player_present_with_id(self, user_id: int) -> bool:
        """Checks if a player with a given Discord user ID already exists in the lobby."""

        for player in self.manager.players:
            if player.discord_user_id == user_id:
                return True

        return False


    def add_player(self, new_player: "Player"):
        """Adds a new player to the lobby.
        
        It assumes the new player is not a duplicate of the ones already inside.

        Args:
            new_player: The new player to be added.
        """

        self.manager.add_player(new_player)
        self.__players_len += 1


    def remove_player_with_id(self, user_id: int) -> Optional["Player"]:
        """Tries to remove a player with a given user Discord ID from the lobby.

        Args:
            user_id: The Discord ID to search with.

        Returns:
            The player that was jsut removed, or `None` if it wasn't present. 
        """

        candidate_index = None
        for i, player in enumerate(self.manager.players):
            if player.discord_user_id == user_id:
                candidate_index = i
                break

        if candidate_index is None:
            return None

        self.__players_len -= 1
        return self.manager.players.pop(candidate_index)


    def player_from_user(self, user: "PossibleUser") -> "Player":
        """Creates a player from a given Discord user."""

        return self.bot.repositories.player.create(user.name, user.id)


    def is_host(self, user: "PossibleUser") -> bool:
        """Checks if a given user is the host of the lobby."""

        return self.user == user
