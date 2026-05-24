from typing import Self

from ..options_base import BaseOptions
from .winning_rounds_enum import WinningRoundsSetting


class ElementRPSOptions(BaseOptions):
    """Options for a game of Element Rock-Paper-Scissors."""

    def __init__(self,
                 *,
                 winning_rounds: WinningRoundsSetting):
        """Initializes the options for a game of Element Rock-Paper-Scissors.
        
        Args:
            winning_rounds: How many won rounds a player must reach to end the game.
        """

        self.winning_rounds: WinningRoundsSetting = winning_rounds


    @classmethod
    def default(cls) -> Self:
        return cls(
            winning_rounds=WinningRoundsSetting.THREE_ROUNDS
        )
