from enum import IntEnum


class WinningRoundsSetting(IntEnum):
    """How many rounds until the game is won."""

    ONE_ROUND = 1
    THREE_ROUNDS = 3
    FIVE_ROUNDS = 5
    SEVEN_ROUNDS = 7
