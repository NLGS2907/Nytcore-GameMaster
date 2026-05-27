from typing import Self

from ..options_base import BaseOptions
from .winning_rounds_enum import WinningRoundsSetting


class ElementRPSOptions(BaseOptions):
    """Options for a game of Element Rock-Paper-Scissors."""

    def __init__(self,
                 *,
                 use_hex_emojis: bool,
                 winning_rounds: WinningRoundsSetting):
        """Initializes the options for a game of Element Rock-Paper-Scissors.
        
        Args:
            winning_rounds: How many won rounds a player must reach to end the game.
        """

        self.use_hex_emojis: bool = use_hex_emojis
        self.winning_rounds: WinningRoundsSetting = winning_rounds


    @classmethod
    def default(cls) -> Self:
        return cls(
            use_hex_emojis=False,
            winning_rounds=WinningRoundsSetting.TWO_ROUNDS
        )
