from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    from datetime import datetime

    from .elements import RPSRoundData
    from .player import Player

RoundsList: TypeAlias = list["RPSRoundData"]


class RPSResult:
    """Model that holds the data of an entire RPS game.
    
    Attributes:
        player_1: The first player of the game.
        player_2: The second player of the game.
        rounds: The details of the rounds played.
        saved: When was the game recorded.
    """

    def __init__(self,
                 id: int,
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

        self._id: int = id
        self._player_1: "Player" = player_1
        self._player_2: "Player" = player_2
        self._rounds: RoundsList = rounds
        self._saved_at: "datetime" = saved
    
    
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
