from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .elements_enum import ElementType
    from .round_result import RPSRoundResult


@dataclass
class RPSRoundData:
    """Helper class to include data from a round of Element RPS.
    
    Attributes:
        player_1_choice: The choice that the first player made in the round.
        player_2_choice: The choice that the second player made in the round.
        result: The result of that round, from the perspective of the first player.
    """

    player_1_choice: Optional["ElementType"]
    player_2_choice: Optional["ElementType"]
    result: "RPSRoundResult"


    def choices_are_null(self) -> bool:
        """Checks if both choices are null."""

        return self.player_1_choice is None and self.player_2_choice is None
