from unittest import TestCase
from unittest.mock import Mock

from gamemaster.models import ElementType, RPSRoundData, RPSRoundResult
from gamemaster.repositories import PlayerRepository, RPSResultRepository


class TestRPSResultRepository(TestCase):
    def setUp(self):
        self.rps_result_repo = RPSResultRepository(Mock(PlayerRepository))


    def test_encodes_rounds_correctly(self):
        round_1 = Mock(RPSRoundData, **{
            "player_1_choice": ElementType.WATER,
            "player_2_choice": ElementType.FIRE,
            "result": RPSRoundResult.VICTORY
        })
        round_2 = Mock(RPSRoundData, **{
            "player_1_choice": ElementType.WIND,
            "player_2_choice": ElementType.FIRE,
            "result": RPSRoundResult.DEFEAT
        })
        encoded_rounds = b"1\x1E"

        self.assertEqual(self.rps_result_repo.encode_rounds([round_1, round_2]), encoded_rounds)


    def test_decodes_rounds_successfully(self):
        expected_round = RPSRoundData(ElementType.WATER, ElementType.IRON, RPSRoundResult.TIE)

        self.assertEqual(self.rps_result_repo.decode_rounds(b"\x2F"), [expected_round])
