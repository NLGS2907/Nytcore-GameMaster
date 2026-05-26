from enum import IntEnum


class RPSRoundResult(IntEnum):
    """The result of a round of Element RPS from the perspective of player 1."""

    DEFEAT = 0
    VICTORY = 1
    TIE = 2
