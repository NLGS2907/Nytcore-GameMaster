from enum import IntEnum


class WinningRoundsSetting(IntEnum):
    """How many rounds until the game is won."""

    ONE_ROUND = 1
    TWO_ROUNDS = 2
    THREE_ROUNDS = 3
    FOUR_ROUNDS = 4
    FIVE_ROUNDS = 5
