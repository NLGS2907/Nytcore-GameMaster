"""Module for managing repositories."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..repositories import IPlayerRepository, IRPSResultRepository


@dataclass
class RepositoryConfiguration:
    """Configuration of repositories.
    
    Attributes:
        player: Player repository.
        rps_result: RPS game results repository.
    """

    player: "IPlayerRepository"
    rps_result: "IRPSResultRepository"
