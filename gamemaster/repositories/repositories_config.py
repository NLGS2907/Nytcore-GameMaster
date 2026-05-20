"""Module for managing repositories."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..repositories import IPlayerRepository


class RepositoryConfiguration:
    """Configuration of repositories.
    
    Attributes:
        player: Player repository.
    """

    def __init__(self, *,
                 player_repository: "IPlayerRepository"):
        """Initializes the configuration.
        
        Args:
            player_repository: A repo that implements the players' interface.
        """

        self._player: "IPlayerRepository" = player_repository


    @property
    def player(self) -> "IPlayerRepository":
        return self._player


    @player.setter
    def player(self, new_player_repo: "IPlayerRepository"):
        self._player = new_player_repo
