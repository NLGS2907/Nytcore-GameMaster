from typing import TYPE_CHECKING, Generator, Optional, TypeAlias

from .elements import RPSRoundData, RPSRoundResult

if TYPE_CHECKING:
    from datetime import datetime

    from .elements import ElementType
    from .player import Player

RoundsList: TypeAlias = list[RPSRoundData]


class RPSResult:
    """Model that holds the data of an entire RPS game.
    
    Attributes:
        player_1: The first player of the game.
        player_2: The second player of the game.
        rounds: The details of the rounds played.
        saved_at: When was the game recorded.
    """

    def __init__(self,
                 id: Optional[int],
                 player_1: "Player",
                 player_2: "Player",
                 rounds: RoundsList,
                 saved: "datetime"):
        """Initializes the RPS game results.
        
        Args:
            id: The underlying id of the dataset.
            player_1: The first player of the game.
            player_2: The second player of the game.
            rounds: The details of the rounds played.
            saved: When was the game recorded.
        """

        self._id: Optional[int] = id
        self._player_1: "Player" = player_1
        self._player_2: "Player" = player_2
        self._rounds: RoundsList = rounds
        self._saved_at: "datetime" = saved



    @property
    def id(self) -> int:
        return self._id

    
    @property
    def player_1(self) -> "Player":
        return self._player_1


    @player_1.setter
    def player_1(self, new_player_1: "Player"):
        self._player_1 = new_player_1
    
    
    @property
    def player_2(self) -> "Player":
        return self._player_2


    @player_2.setter
    def player_2(self, new_player_2: "Player"):
        self._player_2 = new_player_2
    
    
    @property
    def rounds(self) -> RoundsList:
        return self._rounds


    @rounds.setter
    def rounds(self, new_rounds: RoundsList):
        self._rounds = new_rounds
    
    
    @property
    def saved_at(self) -> "datetime":
        return self._saved_at


    @saved_at.setter
    def saved_at(self, new_saved_at: "datetime"):
        self._saved_at = new_saved_at


    def add_data(self,
                 choice_1: Optional["ElementType"],
                 choice_2: Optional["ElementType"],
                 result: RPSRoundResult) -> RPSRoundData:
        """Appends data to the rounds registry.
        
        Args:
            choice_1: The choice of the first player.
            choice_2: The choice of the second player.
            result: The result of that round.

        Returns:
            The data of the round that was just added.
        """

        round_data = RPSRoundData(choice_1, choice_2, result)
        self.rounds.append(round_data)

        return round_data


    def how_many_rounds(self) -> int:
        """Returns the amount of rounds played."""

        return len(self.rounds)


    def last_round(self) -> Optional[RPSRoundData]:
        """Returns the records of the last round played, or `None` if there's no data."""

        if not self.rounds:
            return None

        return self.rounds[-1]


    def determine_winner(self, round_data: RPSRoundData) -> Optional["Player"]:
        """Tries to guess who won the round based on the given data.
        
        Args:
            round_data: The data of the round.

        Returns:
            The player that has won, or `None` if it was a tie.
        """

        if round_data.result == RPSRoundResult.DEFEAT:
            return self.player_2

        if round_data.result == RPSRoundResult.VICTORY:
            return self.player_1

        return None


    def walk_rounds(self) -> Generator[RPSRoundData]:
        """Yields the data from each round of the game."""

        yield from self.rounds


    def last_null_rounds(self, n: int) -> bool:
        """Checks if the last `n` played rounds were 'null'.

        That is, if both choices in that round were not made.

        Args:
            n: The number of last rounds to inspect.

        Returns:
            A boolean indicating if the last `n` rounds are effectively null.
            If `n` has an invalid format or is greater that the history of rounds,
            then it defaults to `False`.
        """

        if n < 1 or n > self.how_many_rounds():
            return False

        for round_data in self.rounds[-n:]:
            if not round_data.choices_are_null():
                return False

        return True
