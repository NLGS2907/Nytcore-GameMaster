from typing import Self

from ..options_base import BaseOptions
from .winning_rounds_enum import WinningRoundsSetting

HEX_EMOJIS_DEFAULT = False
WINNING_ROUNDS_DEFAULT = WinningRoundsSetting.TWO_ROUNDS
ROUND_TIMEOUT_SECS_DEFAULT = 30


class ElementRPSOptions(BaseOptions):
    """Options for a game of Element Rock-Paper-Scissors.
    
    Attributes:
        use_hex_emojis: Wether to use the badge emojis for the elements, or the cropped ones.
                        The badge ones have an hexagonal shape.
        winning_rounds: How many won rounds a player must reach to end the game.
        round_timeout: How much time (in seconds) to wait until the round finishes by itself,
                       choices made or not.
    """

    def __init__(self,
                 *,
                 use_hex_emojis: bool,
                 winning_rounds: WinningRoundsSetting,
                 round_timeout: int):
        """Initializes the options for a game of Element Rock-Paper-Scissors.

        Args:
        use_hex_emojis: Wether to use the badge emojis for the elements, or the cropped ones.
                        The badge ones have an hexagonal shape.
        winning_rounds: How many won rounds a player must reach to end the game.
        round_timeout: How much time (in seconds) to wait until the round finishes by itself,
                       choices made or not.
        """

        self.use_hex_emojis: bool = use_hex_emojis
        self.winning_rounds: WinningRoundsSetting = winning_rounds
        self.round_timeout: int = round_timeout


    @classmethod
    def default(cls) -> Self:
        return cls(
            use_hex_emojis=HEX_EMOJIS_DEFAULT,
            winning_rounds=WINNING_ROUNDS_DEFAULT,
            round_timeout=ROUND_TIMEOUT_SECS_DEFAULT,
        )
