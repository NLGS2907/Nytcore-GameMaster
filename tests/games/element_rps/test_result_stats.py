from unittest import TestCase
from unittest.mock import Mock

from gamemaster.games import RPSResultStats
from gamemaster.models import ElementType, RPSResult, RPSRoundData, RPSRoundResult


class TestRPSResultStats(TestCase):
    def setUp(self):
        self.rps_result_mock = Mock(RPSResult, **{
            "walk_rounds.return_value": (round_data for round_data in [
                Mock(RPSRoundData, **{
                    "player_1_choice": ElementType.FIRE,
                    "player_2_choice": ElementType.WATER,
                    "result": RPSRoundResult.DEFEAT
                }),
                Mock(RPSRoundData, **{
                    "player_1_choice": ElementType.WATER,
                    "player_2_choice": ElementType.IRON,
                    "result": RPSRoundResult.TIE
                }),
                Mock(RPSRoundData, **{
                    "player_1_choice": ElementType.WIND,
                    "player_2_choice": ElementType.IRON,
                    "result": RPSRoundResult.VICTORY
                })
            ])
        })
        self.rps_stats = RPSResultStats(self.rps_result_mock)


    def test_can_count_the_ties(self):
        self.assertEqual(self.rps_stats.ties_count, 1)


    def test_can_detect_favourite_elements(self):
        self.assertCountEqual(self.rps_stats.player_1_favs, [ElementType.FIRE,
                                                             ElementType.WATER,
                                                             ElementType.WIND])
        self.assertCountEqual(self.rps_stats.player_2_favs, [ElementType.IRON])
