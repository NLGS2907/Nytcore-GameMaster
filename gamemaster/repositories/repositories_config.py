"""Module for managing repositories."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..repositories import IPlayerRepository, IRPSResultRepository


class RepositoryConfiguration:
    """Configuration of repositories.
    
    Attributes:
        player: Player repository.
    """

    def __init__(self,
                 *,
                 player_repository: "IPlayerRepository",
                 rps_result_repository: "IRPSResultRepository"):
        """Initializes the configuration.
        
        Args:
            player_repository: A repo that implements the players' interface.
            rps_result_repository: A repo that implements the RPS results' interface.
        """

        self._player: "IPlayerRepository" = player_repository
        self._rps_result: "IRPSResultRepository" = rps_result_repository


    @property
    def player(self) -> "IPlayerRepository":
        return self._player


    @player.setter
    def player(self, new_player_repo: "IPlayerRepository"):
        self._player = new_player_repo


    @property
    def rps_result(self) -> "IRPSResultRepository":
        return self._rps_result


    @rps_result.setter
    def rps_result(self, new_rps_result_repo: "IRPSResultRepository"):
        self._rps_result = new_rps_result_repo
