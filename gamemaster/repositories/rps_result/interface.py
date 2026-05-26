from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeAlias

from ..base_repository import BaseRepository

if TYPE_CHECKING:
    from ...models import RoundsList, RPSResult


EncodedRoundsType: TypeAlias = int


class IRPSResultRepository(BaseRepository["RPSResult"], ABC):
    """Interface for RPS result repositories.
    
    Any repository that wants to deal with RPS games' data must implement these interface.
    """

    @abstractmethod
    def encode_rounds(self, rounds: "RoundsList") -> EncodedRoundsType:
        """Encodes the rounds into a huge number to store.

        Args:
            rounds: The list of rounds to encode.

        Returns:
            A big number encoding all the result of every round.
        """

        raise NotImplementedError


    @abstractmethod
    def decode_rounds(self, result: EncodedRoundsType) -> "RoundsList":
        """Decodes the encoded number back into a list of rounds.

        Args:
            result: The big number to decode.

        Returns:
            A list of all the results of the rounds.
        """

        raise NotImplementedError
