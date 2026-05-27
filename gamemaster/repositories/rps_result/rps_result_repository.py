from typing import TYPE_CHECKING, Optional, TypeAlias

from ...db.datasets import RPSResultDataset
from ...models import ElementType, RPSResult, RPSRoundData, RPSRoundResult
from .interface import EncodedRoundsType, IRPSResultRepository

if TYPE_CHECKING:
    from ...models import RoundsList

_MaybeElement: TypeAlias = Optional[ElementType]
_ENCODE_MAP: dict[_MaybeElement, int] = {None: 0, **{element: element.value
                                                     for element in ElementType}}
_DECODE_MAP: dict[int, _MaybeElement] = {value: key for key, value in _ENCODE_MAP.items()}

CHOICES_PER_OUTCOME: int = 3
CHOICES_PER_PLAYER: int = CHOICES_PER_OUTCOME * len(_ENCODE_MAP)


class RPSResultRepository(IRPSResultRepository):
    @staticmethod
    def dataset_cls():
        return RPSResult


    def _model_to_dataset(self, model: RPSResult) -> RPSResultDataset:
        return RPSResultDataset(
            id=model._id,
            player_1=self._player_repo._model_to_dataset(model.player_1),
            player_2=self._player_repo._model_to_dataset(model.player_2),
            rounds=self.encode_rounds(model.rounds),
            saved=model.saved_at
        )


    def _dataset_to_model(self, dataset: RPSResultDataset) -> RPSResult:
        return RPSResult(
            id=dataset.get_id(),
            player_1=self._player_repo._dataset_to_model(dataset.player_1),
            player_2=self._player_repo._dataset_to_model(dataset.player_2),
            rounds=self.decode_rounds(dataset.rounds),
            saved=dataset.saved
        )


    def encode_rounds(self, rounds: "RoundsList") -> EncodedRoundsType:
        result = []

        for round in rounds:
            result.append(
                sum((
                    _ENCODE_MAP[round.player_1_choice] * CHOICES_PER_PLAYER,
                    _ENCODE_MAP[round.player_2_choice] * CHOICES_PER_OUTCOME,
                    round.result.value
                ))
            )

        return EncodedRoundsType(result)


    def decode_rounds(self, result: EncodedRoundsType) -> "RoundsList":
        rounds = []

        for encoded_round in result:
            player_1_choice = _DECODE_MAP[encoded_round // CHOICES_PER_PLAYER]
            remainder = encoded_round % CHOICES_PER_PLAYER

            player_2_choice = _DECODE_MAP[remainder // CHOICES_PER_OUTCOME]
            outcome = RPSRoundResult(remainder % CHOICES_PER_OUTCOME)

            rounds.append(RPSRoundData(player_1_choice, player_2_choice, outcome))

        return rounds
