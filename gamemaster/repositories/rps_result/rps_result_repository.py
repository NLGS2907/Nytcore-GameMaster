from typing import TYPE_CHECKING

from ...db.datasets import RPSResultDataset
from ...models import ElementType, RPSResult, RPSRoundData, RPSRoundResult
from .interface import IRPSResultRepository

if TYPE_CHECKING:
    from ...models import RoundsList
    from .interface import EncodedRoundsType

BASE_THREE: int = 3
_ENCODE_MAP: dict[ElementType, int] = {
    None: BASE_THREE,
    ElementType.WIND: BASE_THREE + 1,
    ElementType.WATER: BASE_THREE + 2,
    ElementType.IRON: BASE_THREE + 3,
    ElementType.FIRE: BASE_THREE + 4,
    ElementType.ELECTRIC: BASE_THREE + 5
}
_DECODE_MAP: dict[int, ElementType] = {value: key for key, value in _ENCODE_MAP.items()}


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


    @staticmethod
    def _dec_to_base_3(dec: int) -> str:
        """Converts a given decimal number into its representation in base 3."""

        digits = []
        while dec >= BASE_THREE:
            divided = dec // BASE_THREE
            remainder = dec % BASE_THREE

            digits.append(str(remainder))
            dec = divided

        digits.append(str(dec % BASE_THREE))
        return "".join(reversed(digits))


    @staticmethod
    def _base_3_to_dec(num: str) -> int:
        """Converts a string representing a base 3 number back into a decimal."""

        return int(num, BASE_THREE)


    def encode_rounds(self, rounds: "RoundsList") -> "EncodedRoundsType":
        result = []

        for round in rounds:
            result.append(self._dec_to_base_3(_ENCODE_MAP[round.player_1_choice]))
            result.append(self._dec_to_base_3(_ENCODE_MAP[round.player_2_choice]))
            result.append(self._dec_to_base_3(round.result.value))

        return self._base_3_to_dec("".join(result))


    def decode_rounds(self, result: "EncodedRoundsType") -> "RoundsList":
        rounds = []
        res_len = len(result)
        digits_per_data = 5
        for i in range(0, res_len, digits_per_data):
            round_data = result[i:i+digits_per_data]
            rounds.append(RPSRoundData(_DECODE_MAP[self._base_3_to_dec(round_data[:2])],
                                       _DECODE_MAP[self._base_3_to_dec(round_data[2:4])],
                                       RPSRoundResult(self._dec_to_base_3(round_data[4]))))

        return rounds
